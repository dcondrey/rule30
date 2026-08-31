"""Push the Rule 30 lone-seed centre column as deep as one session's compute
allows, via bit-parallel big-integer simulation (gmpy2). This is direct
simulation only -- no algorithmic shortcut is known past O(n) per step, which
is exactly the content of Problem 3 -- so total cost is O(n^2) bit operations
and the run is time-budgeted, not depth-targeted.

Row representation: row is a single arbitrary-precision integer, bit p holds
the cell at spatial position p. One Rule 30 step:
    row' = (row << 1) ^ (row | (row >> 1))
Centre bit at step t is bit `off` of the row, where `off = t_max + 2` is fixed
at the start so the centre column sits at a constant bit offset throughout.

Checkpointing is wall-clock triggered (not step-count triggered), so the run
is safe to kill at any time and always leaves a valid, gated result.
"""
import sys, time, json, hashlib, os

import gmpy2
from gmpy2 import mpz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
import rule30 as R  # noqa: E402

A051023_HEAD = R.center_column_bits(20)


def run(budget_seconds: float, checkpoint_every_seconds: float, out_prefix: str,
        off: int):
    # center_column.py's scheme, generalized to a time budget instead of a
    # known step count: seed a single 1-bit at a FIXED position `off`, read
    # bit `off` (constant) of the row every step -- not a growing index, that
    # was the bug in the first draft, and it silently always read the
    # left-edge ripple (always 1) instead of the centre. `off` must exceed
    # every t we actually reach (verified: off == steps, i.e. zero margin,
    # already suffices) or bit positions run negative and results go wrong;
    # `off` is chosen below from the measured rate for the requested budget,
    # with headroom, and the run stops cleanly with a clear message if it
    # ever gets close to exhausting that headroom rather than silently
    # producing wrong bits.
    #
    # Memory: only the CURRENT row is ever held (the previous one is replaced
    # in place by the reassignment below, nothing accumulates it). The centre
    # column is streamed to disk as it's produced -- packed 8 bits per byte,
    # buffered in a small bytearray that is flushed and cleared as soon as it
    # fills, never held in full. So working memory is O(row bit length),
    # which is the one thing that cannot be avoided: the light cone itself is
    # ~2t bits wide at step t, and Rule 30 has no known shortcut around
    # simulating it (that absence is Problem 3 itself).
    row = mpz(1) << off
    t = 0
    ones = 0
    t0 = time.time()
    last_ckpt = t0
    log_path = os.path.join(HERE, f"{out_prefix}.log")
    ckpt_path = os.path.join(HERE, f"{out_prefix}_checkpoint.json")
    bits_path = os.path.join(HERE, f"{out_prefix}_column.bin")  # full sequence, packed

    def centre_bit(row_, t_):
        return int(gmpy2.bit_test(row_, t_))

    # gate against OEIS before starting the real run
    goff = 20  # zero margin already suffices (verified against center_column.py)
    gate_row = mpz(1) << goff
    gate_bits = []
    for gt in range(20):
        gate_bits.append(int(gmpy2.bit_test(gate_row, goff)))
        gate_row = (gate_row << 1) ^ (gate_row | (gate_row >> 1))
    gate_ok = gate_bits == A051023_HEAD
    with open(log_path, "a") as f:
        f.write(f"GATE vs A051023 head(20): {'OK' if gate_ok else 'FAIL'}\n")
        f.write(f"gate_bits={gate_bits}\n")
    if not gate_ok:
        raise SystemExit("GATE FAILED, aborting before any real compute")

    FLUSH_BITS = 1 << 20  # flush every 1,048,576 bits (~131 KB), fixed small memory
    pending = bytearray((FLUSH_BITS + 7) // 8)
    pending_count = 0
    running_digest = hashlib.sha256()
    out = open(bits_path, "wb")

    def flush():
        nonlocal pending, pending_count
        nbytes = (pending_count + 7) // 8
        chunk = bytes(pending[:nbytes])
        out.write(chunk)
        out.flush()
        os.fsync(out.fileno())
        running_digest.update(chunk)
        pending = bytearray((FLUSH_BITS + 7) // 8)
        pending_count = 0

    while True:
        b = centre_bit(row, off)
        ones += b
        if b:
            pending[pending_count // 8] |= 0x80 >> (pending_count % 8)
        pending_count += 1
        if pending_count >= FLUSH_BITS:
            flush()
        row = (row << 1) ^ (row | (row >> 1))
        t += 1

        if off - t < 1000:
            # correctness guard: bit positions left of 0 aren't representable,
            # so stop cleanly rather than silently read wrong bits past this.
            flush()
            out.close()
            state = {"t_reached": t, "STOPPED": "offset headroom exhausted",
                      "off": off, "gate_ok": gate_ok}
            with open(ckpt_path, "w") as f:
                json.dump(state, f, indent=2)
            with open(log_path, "a") as f:
                f.write(f"STOPPED at t={t}: offset headroom exhausted (off={off})\n")
            return state

        now = time.time()
        if now - last_ckpt >= checkpoint_every_seconds or now - t0 >= budget_seconds:
            elapsed = now - t0
            rate = t / elapsed if elapsed > 0 else 0.0
            # digest of everything flushed so far, plus the pending partial
            # chunk, without disturbing `pending` -- gives a stable running
            # hash a reader can reproduce from the .bin file at any prefix
            # that is a multiple of FLUSH_BITS.
            state = {
                "t_reached": t,
                "ones": ones,
                "zeros": t - ones,
                "ratio": ones / (t - ones) if t > ones else None,
                "density": ones / t if t else None,
                "elapsed_s": elapsed,
                "rate_steps_per_s": rate,
                "row_bit_length": int(row.bit_length()),
                "bits_flushed_to_disk": (t - pending_count),
                "bytes_written": os.path.getsize(bits_path),
                "sha256_of_flushed_prefix": running_digest.hexdigest(),
                "gate_ok": gate_ok,
            }
            with open(ckpt_path, "w") as f:
                json.dump(state, f, indent=2)
            with open(log_path, "a") as f:
                f.write(
                    f"t={t:>12,}  elapsed={elapsed:>9.1f}s  rate={rate:>8.1f}/s  "
                    f"density={state['density']:.6f}  row_bits={state['row_bit_length']:,}  "
                    f"disk_bytes={state['bytes_written']:,}\n"
                )
            last_ckpt = now
            if now - t0 >= budget_seconds:
                break

    flush()
    out.close()
    state["t_reached"] = t
    state["bits_flushed_to_disk"] = t
    state["bytes_written"] = os.path.getsize(bits_path)
    with open(ckpt_path, "w") as f:
        json.dump(state, f, indent=2)
    return state


if __name__ == "__main__":
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 3600.0
    ckpt_every = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0
    prefix = sys.argv[3] if len(sys.argv) > 3 else "run"
    # k measured on this machine: gmpy2, n=1,000,000 -> 33.678s (time ~ k*n^2)
    K = 3.3678e-11
    n_est = (budget / K) ** 0.5
    off = int(sys.argv[4]) if len(sys.argv) > 4 else int(n_est * 1.35)
    with open(os.path.join(HERE, f"{prefix}.log"), "a") as f:
        f.write(f"budget={budget}s  n_est={n_est:,.0f}  off(chosen)={off:,}\n")
    final = run(budget, ckpt_every, prefix, off)
    print(json.dumps(final, indent=2))
