"""SUPERSEDED AND BROKEN. Do not run. Retained for the audit trail only.

Superseded by modal_run_band.py. Two independent defects, either fatal:

  1. It calls rule30_v6 with 8 arguments; the kernel takes 9. The trailing
     `words_per_batch` was added when recording moved to a contiguous k-range.
     The launch raises before any work is done.
  2. Its recording arguments still follow the retired three-lookup-array
     contract: it passes a word index and a bit offset (`gcw`, `gcb`) where
     the current kernel expects `rec_lo_cell` (a cell index) and `n_rec`.
     Fixing (1) alone would produce silently wrong output.

Outputs this script left on the Modal volume rule30-deep are therefore
UNREPRODUCIBLE, not merely suspect, and must not be cited:
    n3000000000_column.bin, n40000000_*, n3000000_*  (8 files)
They predate the recording-ownership fix in rule30_kernel_v6.cu; see
KERNEL-V6-DEFECT.md. The measured throughput quoted below is likewise from
the pre-fix revision and is not a recoverable measurement.

Kernel: v6 (per-lane register chunks + warp shuffles), measured 1.10e14
cell-updates/s on H100, config R=16 H=16 W=4, 512 steps per batch.

Target: n = 3e9, ~11.4 h, ~$45 at $3.95/hr.

Design notes that matter for a run this long:
  * Diamond light cone. To get c_0..c_n we only need cells with
    |x| <= min(t, n-t), so the row is allocated once at n bits and the
    active span grows then shrinks. Halves the work versus a full triangle.
  * Checkpoints go to a Modal Volume every CKPT_MINUTES. A crash costs at
    most that much compute, never the whole run.
  * Resume is automatic: on start we look for the newest checkpoint for this
    target n and continue from it. Re-invoking after any failure is safe.
  * The centre column is streamed to the volume incrementally, packed 8 bits
    per byte, never held whole in host memory beyond a small buffer.
  * Correctness is gated against OEIS A051023 on the GPU before any real
    work, and the first 64 bits of the produced column are re-checked at the
    end of every batch that covers them.

Run:      uv run modal run modal_run_deep.py --n 3000000000
Resume:   identical command; it picks up from the last checkpoint.
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"
image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v6.cu", "/root/rule30_kernel_v6.cu")
)
app = modal.App("rule30-deep-run", image=image)
vol = modal.Volume.from_name("rule30-deep", create_if_missing=True)
VOL = "/data"

A051023_64 = [
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
]

# winning v6 config from the sweep
R, H, WARPS = 16, 16, 4
STEPS_PER_BATCH = 32 * H            # 512
WARP_WORDS = 32 * R                 # 512
USEFUL_PER_WARP = WARP_WORDS - 2 * H
CKPT_MINUTES = 30.0


@app.function(gpu="H100", timeout=24 * 3600, volumes={VOL: vol})
def deep_run(n: int, hours_budget: float = 23.0):
    import os, json, time
    import numpy as np
    import cupy as cp

    tag = f"n{n}"
    ck_path = f"{VOL}/{tag}_state.npz"
    meta_path = f"{VOL}/{tag}_meta.json"
    col_path = f"{VOL}/{tag}_column.bin"

    src = open("/root/rule30_kernel_v6.cu").read()
    opts = (f"-DWORDS_PER_LANE={R}", f"-DHALO_WORDS={H}",
            f"-DWARPS_PER_BLOCK={WARPS}", "-std=c++14")
    mod = cp.RawModule(code=src, options=opts, backend="nvcc")
    kern = mod.get_function("rule30_v6")
    threads = WARPS * 32
    useful_per_block = USEFUL_PER_WARP * WARPS

    # ---------- correctness gate, every invocation ----------
    gw = 16384
    gc = gw * 32 // 2
    gcw, gcb = gc // 32, gc % 32
    ga = cp.zeros(gw, dtype=cp.uint32)
    ga[gcw] = np.uint32(1) << np.uint32(gcb)
    gb = cp.zeros_like(ga)
    gout = cp.zeros(2, dtype=cp.uint32)
    ggrid = (gw + useful_per_block - 1) // useful_per_block
    kern((ggrid,), (threads,),
         (ga, gb, np.uint64(gw), np.int64(gcw), np.int32(gcb),
          gout, np.int32(64), np.int64(0)))
    cp.cuda.Stream.null.synchronize()
    gh = cp.asnumpy(gout)
    gbits = [int((gh[i >> 5] >> (i & 31)) & 1) for i in range(64)]
    if gbits != A051023_64:
        return {"ABORT": "correctness gate failed", "bits": gbits[:16]}

    # ---------- row layout ----------
    # Diamond: allocate the widest the active span ever gets, which is at
    # t = n/2 where it spans n cells. Centre sits in the middle.
    row_cells = n + 64
    n_words = (row_cells + 31) // 32
    n_words = ((n_words + useful_per_block - 1) // useful_per_block) * useful_per_block
    centre_cell = n_words * 32 // 2
    centre_word, centre_bit = centre_cell // 32, centre_cell % 32

    # ---------- resume or start ----------
    a = None
    t_done = 0
    if os.path.exists(ck_path) and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        if meta.get("n") == n and meta.get("n_words") == n_words:
            z = np.load(ck_path)
            a = cp.asarray(z["row"])
            t_done = int(meta["t_done"])
            print(f"RESUMING from t={t_done:,}")
    if a is None:
        a = cp.zeros(n_words, dtype=cp.uint32)
        a[centre_word] = np.uint32(1) << np.uint32(centre_bit)
        t_done = 0
        open(col_path, "wb").close()   # truncate
    b = cp.zeros_like(a)

    total_blocks = n_words // useful_per_block
    cout = cp.zeros(STEPS_PER_BATCH // 32, dtype=cp.uint32)

    def active_blocks(t_start, steps):
        """Blocks covering the diamond |x| <= min(t, n-t) for this batch.

        Use the widest half-width reached during the batch, plus the halo the
        kernel consumes, so nothing the batch reads is left unlaunched.
        """
        t_end = t_start + steps
        half = max(min(t_end, n - t_start), 1) + 32 * H + 64
        half_words = int(half // 32) + 2
        lo_w = max(0, centre_word - half_words)
        hi_w = min(n_words - 1, centre_word + half_words)
        b_lo = lo_w // useful_per_block
        b_hi = hi_w // useful_per_block
        return int(b_lo), int(b_hi - b_lo + 1)

    t0 = time.time()
    last_ck = t0
    verified_head = False
    # bit packer, MSB-first within each byte; `carry` holds a partial byte
    # between flushes so the stream stays exactly t_done bits long.
    packed = bytearray()
    carry = []          # < 8 pending bits

    def add_bits(bs):
        nonlocal carry
        buf = carry + bs
        nfull = len(buf) // 8
        for k in range(nfull):
            byte = 0
            for j in range(8):
                if buf[k * 8 + j]:
                    byte |= 0x80 >> j
            packed.append(byte)
        carry = buf[nfull * 8:]

    def flush_column():
        nonlocal packed
        if packed:
            with open(col_path, "ab") as f:
                f.write(bytes(packed))
            packed = bytearray()

    def checkpoint(t_now):
        flush_column()
        # np.savez appends .npz, so write to an explicit handle to control
        # the exact temp filename, then atomically replace.
        tmp = ck_path + ".tmp"
        with open(tmp, "wb") as fh:
            np.savez(fh, row=cp.asnumpy(a))
        os.replace(tmp, ck_path)
        json.dump({"n": n, "n_words": int(n_words), "t_done": int(t_now),
                   "centre_word": int(centre_word), "centre_bit": int(centre_bit),
                   "elapsed_s": time.time() - t0,
                   "col_bytes": os.path.getsize(col_path)},
                  open(meta_path, "w"), indent=2)
        vol.commit()

    while t_done < n:
        steps = min(STEPS_PER_BATCH, n - t_done)
        cout.fill(0)
        b_off, b_cnt = active_blocks(t_done, steps)
        b_cnt = min(b_cnt, total_blocks - b_off)
        kern((b_cnt,), (threads,),
             (a, b, np.uint64(n_words), np.int64(centre_word),
              np.int32(centre_bit), cout, np.int32(steps), np.int64(b_off)))
        cp.cuda.Stream.null.synchronize()
        a, b = b, a

        host = cp.asnumpy(cout)
        bits = [int((host[i >> 5] >> (i & 31)) & 1) for i in range(steps)]
        if not verified_head and t_done == 0:
            if bits[:64] != A051023_64[:min(64, steps)]:
                return {"ABORT": "produced column disagrees with A051023",
                        "got": bits[:16], "want": A051023_64[:16]}
            verified_head = True
        add_bits(bits)
        t_done += steps

        now = time.time()
        if (now - last_ck) / 60.0 >= CKPT_MINUTES:
            checkpoint(t_done)
            last_ck = now
            rate = t_done / (now - t0)
            print(f"t={t_done:,}/{n:,}  {100*t_done/n:.2f}%  "
                  f"{rate:,.0f} steps/s  eta {(n-t_done)/rate/3600:.2f} h")
        if (now - t0) / 3600.0 >= hours_budget:
            checkpoint(t_done)
            return {"PAUSED_BUDGET": True, "t_done": t_done, "n": n,
                    "elapsed_hours": (now - t0) / 3600.0}

    checkpoint(t_done)
    with open(col_path, "rb") as f:
        data = f.read()
    ones = sum(bin(byte).count("1") for byte in data)
    head = []
    for i in range(min(256, t_done)):
        head.append(int((data[i >> 3] >> (7 - (i & 7))) & 1))
    import hashlib
    return {"COMPLETE": True, "n": n, "t_done": t_done,
            "elapsed_hours": (time.time() - t0) / 3600.0,
            "column_bytes": len(data), "ones": ones,
            "density": ones / t_done,
            "head256": head,
            "sha256": hashlib.sha256(data).hexdigest()}


@app.local_entrypoint()
def main(n: int = 3000000000, hours: float = 23.0):
    import json
    res = deep_run.remote(n, hours)
    print(json.dumps(res, indent=2))
    with open("deep_run_result.json", "w") as f:
        json.dump(res, f, indent=2)
