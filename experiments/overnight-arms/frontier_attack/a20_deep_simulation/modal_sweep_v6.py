"""Sweep v6 (register chunks + warp shuffles) configurations for throughput.

Run:  uv run modal run modal_sweep_v6.py

Two things this does NOT establish, both of which were previously read off it:

  * The gate below is 64 steps on the centre column. It is a smoke test for the
    stencil and the shuffles, not a correctness gate on the generator --
    KERNEL-V6-DEFECT.md's defect first showed at bit 4,631. Full-output
    verification is verify_band.py; a config timing well here is not thereby
    known to be correct.
  * V1_RATE is v1's measured throughput, but v1 was never checked for
    full-output correctness either, and it shares the tiled-halo structure that
    produced the v6 defect. A ratio against it is therefore reported below as
    `speedup_vs_v1_UNVERIFIED_BASELINE` and should not be quoted as a speedup
    over a known-good kernel.

Timing runs with rec_out = nullptr, so the recording path is excluded from the
measurement here exactly as it was before the ownership fix; the fix touches
only that path.
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"
image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v6.cu", "/root/rule30_kernel_v6.cu")
)
app = modal.App("rule30-sweep-v6", image=image)

A051023_64 = [
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
]
V1_RATE = 4.0857661939430e13
USD_HR = 3.95


@app.function(gpu="H100", timeout=1800)
def sweep(bench_words: int = 1 << 22):
    import time, json
    import numpy as np
    import cupy as cp

    src = open("/root/rule30_kernel_v6.cu").read()
    results = []

    # (threads, words_per_thread, steps_per_tile)
    # (words_per_lane R, halo_words H, warps_per_block W)
    configs = [(4, 4, 4), (8, 8, 4), (8, 8, 8), (8, 16, 4),
               (16, 8, 4), (16, 16, 4), (16, 16, 2),
               (8, 4, 8), (4, 8, 8), (16, 32, 2)]

    for R, H, warps in configs:
        threads = warps * 32
        warp_words = 32 * R
        useful = warp_words - 2 * H          # useful words per WARP
        spt = 32 * H
        shared_bytes = warps * warp_words * 4
        rec = {"words_per_lane": R, "halo_words": H, "warps_per_block": warps,
               "threads": threads, "steps_per_batch": spt,
               "warp_words": warp_words, "useful_words_per_warp": useful,
               "shared_KB": shared_bytes / 1024,
               "efficiency": useful / warp_words if warp_words else 0}
        if useful <= 0 or shared_bytes > 160000:
            rec["skipped"] = f"useful={useful} shared={shared_bytes}"
            results.append(rec); continue
        try:
            opts = (f"-DWORDS_PER_LANE={R}", f"-DHALO_WORDS={H}",
                    f"-DWARPS_PER_BLOCK={warps}", "-std=c++14")
            mod = cp.RawModule(code=src, options=opts, backend="nvcc")
            k = mod.get_function("rule30_v6")
        except Exception as e:
            rec["compile_error"] = str(e)[:200]
            results.append(rec); continue

        useful_per_block = useful * warps
        N_CHECK = min(64, spt)
        words = max(useful_per_block * 4, 16384)
        centre_cell = words * 32 // 2
        cw, cb = centre_cell // 32, centre_cell % 32
        a = cp.zeros(words, dtype=cp.uint32)
        a[cw] = np.uint32(1) << np.uint32(cb)
        b = cp.zeros_like(a)
        wpb = spt // 32                       # words_per_batch, >= 2 for spt >= 64
        cout = cp.zeros(wpb, dtype=cp.uint32)
        grid = (words + useful_per_block - 1) // useful_per_block
        # 9-arg band signature: rec_lo_cell is a CELL index, n_rec columns,
        # then block_offset and words_per_batch. The 7-arg call this replaced
        # predated the band-recording kernel and could no longer even launch.
        k((grid,), (threads,),
          (a, b, np.uint64(words), np.int64(centre_cell), np.int32(1),
           cout, np.int32(N_CHECK), np.int64(0), np.int32(wpb)))
        cp.cuda.Stream.null.synchronize()
        host = cp.asnumpy(cout)
        bits = [int((host[i >> 5] >> (i & 31)) & 1) for i in range(N_CHECK)]
        rec["gate_ok"] = bits == A051023_64[:N_CHECK]
        if not rec["gate_ok"]:
            rec["gate_head"] = bits[:16]; rec["expected_head"] = A051023_64[:16]
            results.append(rec); continue

        a = cp.random.randint(0, 2**32, size=bench_words, dtype=cp.uint32)
        b = cp.zeros_like(a)
        grid = (bench_words + useful_per_block - 1) // useful_per_block
        nbatch = 8
        for _ in range(2):
            k((grid,), (threads,),
              (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
               None, np.int32(spt), np.int64(0), np.int32(0)))
        cp.cuda.Stream.null.synchronize()
        t0 = time.time()
        for _ in range(nbatch):
            k((grid,), (threads,),
              (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
               None, np.int32(spt), np.int64(0), np.int32(0)))
            a, b = b, a
        cp.cuda.Stream.null.synchronize()
        dt = time.time() - t0
        rate = bench_words * 32 * nbatch * spt / dt
        rec["cellsteps_per_s"] = rate
        # v1 was never full-output checked and shares the tiled-halo structure
        # that produced the v6 defect, so this ratio is not a speedup over a
        # known-good kernel. The absolute rate is the honest number.
        rec["speedup_vs_v1_UNVERIFIED_BASELINE"] = rate / V1_RATE
        results.append(rec)

    ok = [r for r in results if r.get("gate_ok") and "cellsteps_per_s" in r]
    ok.sort(key=lambda r: -r["cellsteps_per_s"])
    best = ok[0] if ok else None
    out = {"results": results, "best": best, "v1_rate": V1_RATE}
    if best:
        rate = best["cellsteps_per_s"]
        out["projections_best"] = {
            lab: {"hours": n * n / 2 / rate / 3600,
                  "usd": n * n / 2 / rate / 3600 * USD_HR}
            for n, lab in [(1e9, "1e9"), (2e9, "2e9"), (3e9, "3e9"),
                           (4e9, "4e9"), (5e9, "5e9")]
        }
    print(json.dumps(out, indent=2))
    return out


@app.local_entrypoint()
def main():
    import json
    res = sweep.remote()
    with open("sweep_v6_result.json", "w") as f:
        json.dump(res, f, indent=2)
