"""Deep Rule 30 run recording a BAND of adjacent columns, checkpointed.

Why a band and not just the centre:
  * columns 0 and 1 are the width-two trace, the object of Jen 1990 Prop. 3
    and Kopra 2023 Thm 3.5;
  * r_t on the zero set {t : c_t = 0} is exactly register row 1 (R1), the
    tree's best open route, and a1's named Lemma Z;
  * two adjacent columns determine the ENTIRE left half-plane offline via
    col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t)).
They do NOT make the run resumable (Rule 30 is not right-permutive, so the
right half is unrecoverable); the row checkpoint is what makes it resumable.

File format, per column k, in n{N}_col{signed offset}.bin:
  little-endian uint32 words; step i is bit (i & 31) of word (i >> 5),
  LSB-first. Batches are STEPS_PER_BATCH=512 steps = exactly 16 words, so
  batches concatenate with no bit-shifting and the stream is exactly
  ceil(t_done/32) words long.

Run:     uv run modal run modal_run_band.py --n 3000000000
Resume:  identical command.
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"
image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v6.cu", "/root/rule30_kernel_v6.cu")
    .add_local_file("band_layout.py", "/root/band_layout.py")
)
app = modal.App("rule30-band-run", image=image)
vol = modal.Volume.from_name("rule30-deep", create_if_missing=True)
VOL = "/data"

A051023_64 = [
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
]

# Layout lives in band_layout.py so the host-side ownership mirror and the
# nvcc -D flags cannot drift apart; it is stdlib-only and ships in the image.
from band_layout import (  # noqa: E402
    R, H, WARPS, STEPS_PER_BATCH, USEFUL_PER_WARP, WORDS_PER_BATCH,
)

CKPT_MINUTES = 30.0


@app.function(gpu="H100", timeout=24 * 3600, volumes={VOL: vol})
def band_run(n: int, half_width: int = 4, hours_budget: float = 23.0):
    """Records columns x = -half_width .. +half_width (2*hw+1 columns)."""
    import os, sys, json, time, hashlib
    import numpy as np
    import cupy as cp

    sys.path.insert(0, "/root")
    from band_layout import assert_unique_claimants

    n_rec = 2 * half_width + 1
    tag = f"band_n{n}_w{half_width}"
    ck_path = f"{VOL}/{tag}_state.npz"
    meta_path = f"{VOL}/{tag}_meta.json"
    col_paths = {k: f"{VOL}/{tag}_col{k - half_width:+d}.bin"
                 for k in range(n_rec)}

    src = open("/root/rule30_kernel_v6.cu").read()
    opts = (f"-DWORDS_PER_LANE={R}", f"-DHALO_WORDS={H}",
            f"-DWARPS_PER_BLOCK={WARPS}", "-DMAX_REC=16", "-std=c++14")
    mod = cp.RawModule(code=src, options=opts, backend="nvcc")
    kern = mod.get_function("rule30_v6")
    threads = WARPS * 32
    useful_per_block = USEFUL_PER_WARP * WARPS

    # ---------- smoke gate on the centre column ----------
    # This checks the stencil, the shuffles and the recording indices. It is NOT
    # a correctness gate on the generator and must not be reported as one: it is
    # 64 steps, and the defect it failed to catch first showed at bit 4,631 at a
    # rate of 5e-4. No 64-step prefix check can see that, whatever geometry it
    # is given. Full-output verification is verify_band.py (transduction across
    # the band + density + cross-run identity) and crosscheck_wdr.py (absolute,
    # centre column, to 1e9 bits).
    gw = 16384
    gc = gw * 32 // 2
    ga = cp.zeros(gw, dtype=cp.uint32)
    ga[gc // 32] = np.uint32(1) << np.uint32(gc % 32)
    gb = cp.zeros_like(ga)
    gout = cp.zeros(3 * WORDS_PER_BATCH, dtype=cp.uint32)
    ggrid = (gw + useful_per_block - 1) // useful_per_block
    kern((ggrid,), (threads,),
         (ga, gb, np.uint64(gw), np.int64(gc - 1), np.int32(3),
          gout, np.int32(64), np.int64(0), np.int32(WORDS_PER_BATCH)))
    cp.cuda.Stream.null.synchronize()
    gh = cp.asnumpy(gout)
    # column index 1 of the 3 recorded is the centre (gc-1, gc, gc+1)
    cbits = [int((gh[1 * WORDS_PER_BATCH + (i >> 5)] >> (i & 31)) & 1)
             for i in range(64)]
    if cbits != A051023_64:
        return {"ABORT": "gate failed", "got": cbits[:16],
                "want": A051023_64[:16]}

    # ---------- layout ----------
    row_cells = n + 64
    n_words = (row_cells + 31) // 32
    n_words = ((n_words + useful_per_block - 1) // useful_per_block) * useful_per_block
    centre_cell = n_words * 32 // 2
    rec_lo_cell = centre_cell - half_width

    # ---------- resume or start ----------
    a = None
    t_done = 0
    if os.path.exists(ck_path) and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        if meta.get("n") == n and meta.get("n_words") == n_words \
           and meta.get("half_width") == half_width:
            a = cp.asarray(np.load(ck_path)["row"])
            t_done = int(meta["t_done"])
            print(f"RESUMING from t={t_done:,}", flush=True)
    if a is None:
        a = cp.zeros(n_words, dtype=cp.uint32)
        a[centre_cell // 32] = np.uint32(1) << np.uint32(centre_cell % 32)
        t_done = 0
        for p in col_paths.values():
            open(p, "wb").close()
    b = cp.zeros_like(a)

    total_blocks = n_words // useful_per_block
    rec = cp.zeros(n_rec * WORDS_PER_BATCH, dtype=cp.uint32)
    bufs = {k: bytearray() for k in range(n_rec)}

    def active_blocks(t_start, steps):
        t_end = t_start + steps
        half = max(min(t_end, n - t_start), 1) + 32 * H + 64
        hw = int(half // 32) + 2
        lo_w = max(0, centre_cell // 32 - hw)
        hi_w = min(n_words - 1, centre_cell // 32 + hw)
        b_lo = lo_w // useful_per_block
        b_hi = hi_w // useful_per_block
        return int(b_lo), int(b_hi - b_lo + 1)

    t0 = time.time()
    last_ck = t0

    def flush():
        for k, buf in bufs.items():
            if buf:
                with open(col_paths[k], "ab") as f:
                    f.write(bytes(buf))
                buf.clear()

    def checkpoint(t_now):
        flush()
        tmp = ck_path + ".tmp"
        with open(tmp, "wb") as fh:
            np.savez(fh, row=cp.asnumpy(a))
        os.replace(tmp, ck_path)
        json.dump({"n": n, "n_words": int(n_words), "t_done": int(t_now),
                   "half_width": half_width, "n_rec": n_rec,
                   "centre_cell": int(centre_cell),
                   "steps_per_batch": STEPS_PER_BATCH,
                   "format": "uint32 LE, step i = bit (i&31) of word (i>>5)",
                   "elapsed_s": time.time() - t0},
                  open(meta_path, "w"), indent=2)
        vol.commit()

    verified = False
    # The recorded band always straddles a tile edge (centre_cell is a multiple
    # of 32*USEFUL_PER_WARP by construction), which is what made the pre-fix
    # double-claim structural rather than unlucky. Ownership is pure arithmetic,
    # so settle it on the host for every distinct launch window instead of
    # hoping a prefix gate notices. Windows repeat for ~120 consecutive batches,
    # hence the cache.
    checked_windows: set[tuple[int, int]] = set()

    while t_done < n:
        steps = min(STEPS_PER_BATCH, n - t_done)
        rec.fill(0)
        b_off, b_cnt = active_blocks(t_done, steps)
        b_cnt = min(b_cnt, total_blocks - b_off)
        if (b_off, b_cnt) not in checked_windows:
            assert_unique_claimants(rec_lo_cell, n_rec, b_off, b_cnt)
            checked_windows.add((b_off, b_cnt))
        kern((b_cnt,), (threads,),
             (a, b, np.uint64(n_words), np.int64(rec_lo_cell),
              np.int32(n_rec), rec, np.int32(steps), np.int64(b_off),
              np.int32(WORDS_PER_BATCH)))
        cp.cuda.Stream.null.synchronize()
        a, b = b, a

        host = cp.asnumpy(rec)
        if not verified and t_done == 0:
            cb = [int((host[half_width * WORDS_PER_BATCH + (i >> 5)]
                       >> (i & 31)) & 1) for i in range(min(64, steps))]
            if cb != A051023_64[:len(cb)]:
                return {"ABORT": "stream disagrees with A051023",
                        "got": cb[:16]}
            verified = True

        # whole batches are 16 words exactly, so raw append needs no shifting
        nw = (steps + 31) // 32
        for k in range(n_rec):
            seg = host[k * WORDS_PER_BATCH: k * WORDS_PER_BATCH + nw]
            bufs[k].extend(seg.tobytes())
        t_done += steps

        now = time.time()
        if (now - last_ck) / 60.0 >= CKPT_MINUTES:
            checkpoint(t_done)
            last_ck = now
            rate = t_done / (now - t0)
            print(f"t={t_done:,}/{n:,} {100*t_done/n:.2f}% "
                  f"{rate:,.0f} st/s eta {(n-t_done)/rate/3600:.2f}h",
                  flush=True)
        if (now - t0) / 3600.0 >= hours_budget:
            checkpoint(t_done)
            return {"PAUSED_BUDGET": True, "t_done": t_done, "n": n,
                    "elapsed_hours": (now - t0) / 3600.0}

    checkpoint(t_done)
    summary = {"COMPLETE": True, "n": n, "t_done": t_done,
               "half_width": half_width, "n_rec": n_rec,
               "elapsed_hours": (time.time() - t0) / 3600.0, "columns": {}}
    # popcount via a 256-entry table over numpy, not a Python loop: the naive
    # version walks 3.4 GB one byte at a time in the interpreter.
    POPC = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint16)
    for k in range(n_rec):
        data = open(col_paths[k], "rb").read()
        ones = int(POPC[np.frombuffer(data, dtype=np.uint8)].sum(dtype=np.int64))
        head = [int((int.from_bytes(data[4 * (i >> 5):4 * (i >> 5) + 4],
                                    "little") >> (i & 31)) & 1)
                for i in range(min(64, t_done))]
        summary["columns"][f"{k - half_width:+d}"] = {
            "bytes": len(data), "ones": ones, "density": ones / t_done,
            "sha256": hashlib.sha256(data).hexdigest()[:32],
            "head64": head,
        }
    centre = open(col_paths[half_width], "rb").read()
    summary["centre_head256"] = [
        int((int.from_bytes(centre[4 * (i >> 5):4 * (i >> 5) + 4], "little")
             >> (i & 31)) & 1) for i in range(256)]
    return summary


@app.local_entrypoint()
def main(n: int = 3000000000, half_width: int = 4, hours: float = 23.0):
    import json
    res = band_run.remote(n, half_width, hours)
    print(json.dumps(res, indent=2)[:4000])
    # keyed by run, so validation runs can go in parallel without clobbering
    # each other's result file
    with open(f"band_run_result_n{n}_w{half_width}.json", "w") as f:
        json.dump(res, f, indent=2)
