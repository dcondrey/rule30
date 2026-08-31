"""Calibration for the v2 Rule 30 kernel (uint64 + register blocking).

Compares v2 against the measured v1 baseline (4.0857e13 cell-updates/s on
H100), gates correctness against OEIS A051023 first, and projects cost for a
range of target depths. Charter stage: calibration.

Run:  uv run modal run modal_calibrate_v2.py
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"

image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v2.cu", "/root/rule30_kernel_v2.cu")
)

app = modal.App("rule30-calibration-v2", image=image)

A051023_64 = [
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
]

V1_RATE = 4.0857661939430e13  # measured, cell-updates/s
USD_HR = 3.95


@app.function(gpu="H100", timeout=1200)
def calibrate_v2(bench_words: int = 1 << 21, bench_steps: int = 4096):
    import time
    import json
    import numpy as np
    import cupy as cp

    src = open("/root/rule30_kernel_v2.cu").read()

    THREADS = 256
    WPT = 8               # words per thread
    STEPS_PER_TILE = 256
    TILE_WORDS = THREADS * WPT
    HALO_WORDS = (STEPS_PER_TILE + 63) // 64
    USEFUL_WORDS = TILE_WORDS - 2 * HALO_WORDS

    opts = (
        f"-DTHREADS_PER_BLOCK={THREADS}",
        f"-DWORDS_PER_THREAD={WPT}",
        f"-DSTEPS_PER_TILE={STEPS_PER_TILE}",
        "-std=c++14",
    )
    mod = cp.RawModule(code=src, options=opts, backend="nvcc")
    k_v2 = mod.get_function("rule30_v2")

    props = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    out = {
        "gpu": props["name"].decode(),
        "threads": THREADS, "words_per_thread": WPT,
        "steps_per_tile": STEPS_PER_TILE,
        "tile_words": TILE_WORDS, "halo_words": HALO_WORDS,
        "useful_words": USEFUL_WORDS,
        "halo_efficiency": USEFUL_WORDS / TILE_WORDS,
    }

    # ---------- correctness gate ----------
    N_CHECK = 64
    words = TILE_WORDS  # one tile is plenty for 64 steps
    centre_cell = words * 64 // 2
    centre_word, centre_bit = centre_cell // 64, centre_cell % 64

    a = cp.zeros(words, dtype=cp.uint64)
    a[centre_word] = np.uint64(1) << np.uint64(centre_bit)
    b = cp.zeros_like(a)
    cout = cp.zeros((N_CHECK + 31) // 32, dtype=cp.uint32)

    grid = (words + USEFUL_WORDS - 1) // USEFUL_WORDS
    k_v2((grid,), (THREADS,),
         (a, b, np.uint64(words), np.int64(centre_word), np.int32(centre_bit),
          cout, np.int32(N_CHECK)))
    cp.cuda.Stream.null.synchronize()

    host = cp.asnumpy(cout)
    bits = [int((host[i >> 5] >> (i & 31)) & 1) for i in range(N_CHECK)]
    out["gate_ok"] = bits == A051023_64
    out["gate_gpu_bits_head"] = bits[:20]
    if not out["gate_ok"]:
        out["gate_expected_head"] = A051023_64[:20]
        out["ABORTED"] = "v2 correctness gate failed; no benchmark run"
        print(json.dumps(out, indent=2))
        return out

    # ---------- throughput ----------
    a = cp.random.randint(0, 2**63, size=bench_words, dtype=cp.uint64)
    b = cp.zeros_like(a)
    grid = (bench_words + USEFUL_WORDS - 1) // USEFUL_WORDS
    nbatch = bench_steps // STEPS_PER_TILE

    for _ in range(2):
        k_v2((grid,), (THREADS,),
             (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
              None, np.int32(STEPS_PER_TILE)))
    cp.cuda.Stream.null.synchronize()

    t0 = time.time()
    for _ in range(nbatch):
        k_v2((grid,), (THREADS,),
             (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
              None, np.int32(STEPS_PER_TILE)))
        a, b = b, a
    cp.cuda.Stream.null.synchronize()
    dt = time.time() - t0

    cells = bench_words * 64
    rate = cells * (nbatch * STEPS_PER_TILE) / dt
    out["v2_seconds"] = dt
    out["v2_cellsteps_per_s"] = rate
    out["v1_cellsteps_per_s"] = V1_RATE
    out["speedup_over_v1"] = rate / V1_RATE

    # ---------- projections ----------
    proj = {}
    for n, label in [(1e9, "1e9"), (2e9, "2e9"), (3e9, "3e9"),
                     (4e9, "4e9"), (5e9, "5e9"), (1e10, "1e10")]:
        work = n * n / 2          # diamond light cone
        secs = work / rate
        proj[label] = {
            "hours": secs / 3600,
            "usd": secs / 3600 * USD_HR,
            "peak_row_MB": n / 8 / 1e6,
        }
    out["projections"] = proj

    print(json.dumps(out, indent=2))
    return out


@app.local_entrypoint()
def main():
    import json
    res = calibrate_v2.remote()
    with open("calibration_v2_result.json", "w") as f:
        json.dump(res, f, indent=2)
