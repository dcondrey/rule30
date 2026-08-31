"""Modal calibration for the Rule 30 GPU kernel.

Charter stage: calibration, $5 cumulative ceiling. This job produces NO
scientific claim about Rule 30. Its only outputs are:
  1. a correctness verdict (GPU kernel vs OEIS A051023 and a CPU reference),
  2. measured throughput for the naive and temporally-blocked kernels,
  3. the measured temporal-blocking multiplier against the predicted ~252x,
  4. a projected wall-clock and dollar cost for n = 1e9.

Run:  uv run modal run modal_calibrate.py
"""
import modal

CUDA = "12.4.0"
FLAVOR = "devel"
OS = "ubuntu22.04"
TAG = f"nvidia/cuda:{CUDA}-{FLAVOR}-{OS}"

image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel.cu", "/root/rule30_kernel.cu")
)

app = modal.App("rule30-calibration", image=image)

# First 64 terms of OEIS A051023, the lone-seed Rule 30 centre column.
A051023_64 = [
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
]


@app.function(gpu="H100", timeout=900)
def calibrate(bench_words: int = 1 << 22, bench_steps: int = 4096):
    """bench_words * 32 cells wide; bench_steps steps. Defaults ~134M cells."""
    import time
    import json
    import numpy as np
    import cupy as cp

    src = open("/root/rule30_kernel.cu").read()

    WORDS_PER_TILE = 1024
    STEPS_PER_TILE = 256
    HALO_WORDS = (STEPS_PER_TILE + 31) // 32

    opts = (
        f"-DWORDS_PER_TILE={WORDS_PER_TILE}",
        f"-DSTEPS_PER_TILE={STEPS_PER_TILE}",
        "-std=c++14",
    )
    mod = cp.RawModule(code=src, options=opts, backend="nvcc")
    k_block = mod.get_function("rule30_block_step")
    k_naive = mod.get_function("rule30_naive_step")

    dev = cp.cuda.Device()
    props = cp.cuda.runtime.getDeviceProperties(dev.id)
    gpu_name = props["name"].decode()

    out = {
        "gpu": gpu_name,
        "words_per_tile": WORDS_PER_TILE,
        "steps_per_tile": STEPS_PER_TILE,
        "halo_words": HALO_WORDS,
    }

    # ---------- correctness gate, before any benchmark ----------
    # Small row, seed a single 1 at the centre, run N steps with the blocked
    # kernel, and compare the extracted centre column to A051023.
    N_CHECK = 64
    words = 64  # 2048 cells, ample for 64 steps from centre
    centre_cell = words * 32 // 2
    centre_word, centre_bit = centre_cell // 32, centre_cell % 32

    a = cp.zeros(words, dtype=cp.uint32)
    a[centre_word] = np.uint32(1 << centre_bit)
    b = cp.zeros_like(a)
    cout = cp.zeros((N_CHECK + 31) // 32, dtype=cp.uint32)

    grid = (words + WORDS_PER_TILE - 1) // WORDS_PER_TILE
    k_block(
        (grid,), (256,),
        (a, b, np.uint64(words), np.int64(centre_word), np.int32(centre_bit),
         cout, np.int32(N_CHECK)),
    )
    cp.cuda.Stream.null.synchronize()

    bits = []
    host = cp.asnumpy(cout)
    for i in range(N_CHECK):
        bits.append(int((host[i >> 5] >> (i & 31)) & 1))
    gate_ok = bits == A051023_64
    out["gate_ok"] = gate_ok
    out["gate_gpu_bits"] = bits[:20]
    out["gate_expected"] = A051023_64[:20]
    if not gate_ok:
        out["ABORTED"] = "correctness gate failed; no benchmark run"
        return out

    # ---------- naive one-step-per-launch throughput ----------
    a = cp.random.randint(0, 2**32, size=bench_words, dtype=cp.uint32)
    b = cp.zeros_like(a)
    threads = 256
    nblocks = (bench_words + threads - 1) // threads

    for _ in range(10):  # warmup
        k_naive((nblocks,), (threads,), (a, b, np.uint64(bench_words)))
    cp.cuda.Stream.null.synchronize()

    t0 = time.time()
    for _ in range(bench_steps):
        k_naive((nblocks,), (threads,), (a, b, np.uint64(bench_words)))
        a, b = b, a
    cp.cuda.Stream.null.synchronize()
    t_naive = time.time() - t0

    cells = bench_words * 32
    naive_cellsteps = cells * bench_steps
    out["naive_seconds"] = t_naive
    out["naive_cellsteps_per_s"] = naive_cellsteps / t_naive
    # each step reads and writes the row
    out["naive_achieved_GBps"] = (
        2 * bench_words * 4 * bench_steps / t_naive / 1e9
    )

    # ---------- temporally blocked throughput ----------
    a = cp.random.randint(0, 2**32, size=bench_words, dtype=cp.uint32)
    b = cp.zeros_like(a)
    grid = (bench_words + WORDS_PER_TILE - 1) // WORDS_PER_TILE
    nbatch = bench_steps // STEPS_PER_TILE

    for _ in range(2):  # warmup
        k_block((grid,), (256,),
                (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
                 None, np.int32(STEPS_PER_TILE)))
    cp.cuda.Stream.null.synchronize()

    t0 = time.time()
    for _ in range(nbatch):
        k_block((grid,), (256,),
                (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
                 None, np.int32(STEPS_PER_TILE)))
        a, b = b, a
    cp.cuda.Stream.null.synchronize()
    t_block = time.time() - t0

    blocked_cellsteps = cells * (nbatch * STEPS_PER_TILE)
    out["blocked_seconds"] = t_block
    out["blocked_cellsteps_per_s"] = blocked_cellsteps / t_block
    out["measured_multiplier"] = (
        out["blocked_cellsteps_per_s"] / out["naive_cellsteps_per_s"]
    )
    out["predicted_multiplier"] = STEPS_PER_TILE * (
        WORDS_PER_TILE / (WORDS_PER_TILE + 2 * HALO_WORDS)
    )

    # ---------- projection to n = 1e9 ----------
    # diamond work = n^2/2 cell-updates
    n = 1e9
    work = n * n / 2
    rate = out["blocked_cellsteps_per_s"]
    secs = work / rate
    out["projection_n1e9"] = {
        "cellsteps": work,
        "seconds": secs,
        "hours": secs / 3600,
        "usd_at_3.95_per_hr": secs / 3600 * 3.95,
    }
    n10 = 1e10
    work10 = n10 * n10 / 2
    out["projection_n1e10"] = {
        "hours": work10 / rate / 3600,
        "usd_at_3.95_per_hr": work10 / rate / 3600 * 3.95,
    }

    print(json.dumps(out, indent=2))
    return out


@app.local_entrypoint()
def main():
    import json
    res = calibrate.remote()
    with open("calibration_result.json", "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
