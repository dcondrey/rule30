"""Sweep v4 (contiguous chunks, ping-pong shared, 1 sync/step) against the
v1 baseline. Gates every config on OEIS A051023 before timing it.

Run:  uv run modal run modal_sweep_v4.py
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"
image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v5.cu", "/root/rule30_kernel_v5.cu")
)
app = modal.App("rule30-sweep-v5", image=image)

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

    src = open("/root/rule30_kernel_v5.cu").read()
    results = []

    # (threads, words_per_thread, steps_per_tile)
    # (warps_per_block, halo_lanes)
    configs = [(4, 1), (4, 2), (4, 4), (8, 1), (8, 2), (8, 4),
               (16, 2), (16, 4), (8, 8), (4, 8)]

    for warps, halo in configs:
        threads = warps * 32
        useful_lanes = 32 - 2 * halo
        spt = 32 * halo
        useful = warps * useful_lanes          # useful words per block
        rec = {"warps_per_block": warps, "halo_lanes": halo,
               "threads": threads, "steps_per_batch": spt,
               "useful_lanes": useful_lanes,
               "useful_words_per_block": useful,
               "lane_efficiency": useful_lanes / 32.0}
        if useful_lanes <= 0:
            rec["skipped"] = "halo too large"
            results.append(rec); continue
        try:
            opts = (f"-DWARPS_PER_BLOCK={warps}", f"-DHALO_LANES={halo}",
                    "-std=c++14")
            mod = cp.RawModule(code=src, options=opts, backend="nvcc")
            k = mod.get_function("rule30_v5")
        except Exception as e:
            rec["compile_error"] = str(e)[:200]
            results.append(rec); continue

        N_CHECK = min(64, spt)
        words = max(useful * 4, 8192)
        centre_cell = words * 32 // 2
        cw, cb = centre_cell // 32, centre_cell % 32
        a = cp.zeros(words, dtype=cp.uint32)
        a[cw] = np.uint32(1) << np.uint32(cb)
        b = cp.zeros_like(a)
        cout = cp.zeros(2, dtype=cp.uint32)
        grid = (words + useful - 1) // useful
        k((grid,), (threads,),
          (a, b, np.uint64(words), np.int64(cw), np.int32(cb),
           cout, np.int32(N_CHECK)))
        cp.cuda.Stream.null.synchronize()
        host = cp.asnumpy(cout)
        bits = [int((host[i >> 5] >> (i & 31)) & 1) for i in range(N_CHECK)]
        rec["gate_ok"] = bits == A051023_64[:N_CHECK]
        if not rec["gate_ok"]:
            rec["gate_head"] = bits[:16]
            rec["expected_head"] = A051023_64[:16]
            results.append(rec); continue

        a = cp.random.randint(0, 2**32, size=bench_words, dtype=cp.uint32)
        b = cp.zeros_like(a)
        grid = (bench_words + useful - 1) // useful
        nbatch = 16
        for _ in range(2):
            k((grid,), (threads,),
              (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
               None, np.int32(spt)))
        cp.cuda.Stream.null.synchronize()
        t0 = time.time()
        for _ in range(nbatch):
            k((grid,), (threads,),
              (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
               None, np.int32(spt)))
            a, b = b, a
        cp.cuda.Stream.null.synchronize()
        dt = time.time() - t0
        rate = bench_words * 32 * nbatch * spt / dt
        rec["cellsteps_per_s"] = rate
        rec["speedup_vs_v1"] = rate / V1_RATE
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
    with open("sweep_v5_result.json", "w") as f:
        json.dump(res, f, indent=2)
