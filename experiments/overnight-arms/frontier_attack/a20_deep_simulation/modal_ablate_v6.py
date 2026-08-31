"""Isolate what the v6 throughput number actually measures.

Context. `KERNEL-V6-DEFECT.md` records 1.10e14 cell-updates/s for v6 and calls
it void because it was measured on a kernel that produced wrong bits. Re-timing
the FIXED kernel gives ~2.7e13, a ~4x gap, and the obvious reading -- "the fix
cost 4x" -- is almost certainly wrong: the benchmark passes rec_out = nullptr,
so the entire ownership block the fix lives in is skipped at runtime.

The competing explanation is that the 1.10e14 was measured at 18:40 against a
kernel that had NO band-recording code at all (band recording was added to the
.cu at 20:36, and `modal_sweep_v6.py` still called the old 7-argument signature
until it was updated, so it could not even have launched the later kernel). The
recording code declares three MAX_REC-element int arrays that are dynamically
indexed, which forces them to local memory and costs occupancy whether or not
any recording happens.

Four variants, one harness, same GPU, same run -- so the comparison is not
across machines or across days:

  fixed             the kernel as it stands
  array_form        the recording state as three MAX_REC lookup arrays indexed
                    by a runtime m, plus a dynamic index into the hot register
                    array r; this is what the kernel did before, and it prices
                    the difference
  prefix_ownership  ownership test reverted to the pre-fix predicate; this is
                    the ONLY difference, so it prices the correctness fix itself
  no_recording      recording code removed entirely; the ceiling, and an
                    approximation of the pre-band kernel 1.10e14 came from

What this measured, in order, because the first answer was wrong:

  1. The correctness fix costs nothing: 1.00x. It lives inside a block the
     benchmark skips (rec_out = nullptr).
  2. Removing ONLY the dynamic index into r, keeping the arrays, also bought
     nothing: 1.02x, local_size_bytes still 256. The arrays were the anchor.
  3. Dropping the arrays as well -- the recorded cells are consecutive, so the
     owned columns are a contiguous RANGE and slot/bit are arithmetic in k --
     took local_size_bytes to 0 and threw 3.97x. Band recording now costs 1.03x
     against removing it outright, where it used to cost 4.03x.

Variants are made by exact string surgery on the source, each assertion checking
the substring occurs exactly once, so a silently-missed edit cannot be reported
as a result.

Run:  uv run modal run modal_ablate_v6.py
"""
import modal

TAG = "nvidia/cuda:12.4.0-devel-ubuntu22.04"
image = (
    modal.Image.from_registry(TAG, add_python="3.11")
    .apt_install("build-essential")
    .pip_install("numpy", "cupy-cuda12x")
    .add_local_file("rule30_kernel_v6.cu", "/root/rule30_kernel_v6.cu")
)
app = modal.App("rule30-ablate-v6", image=image)

OWNERSHIP_FIXED = """            if (wl >= HALO_WORDS && wl < HALO_WORDS + USEFUL_WORDS &&
                wl >= base && wl < base + WORDS_PER_LANE) {"""
OWNERSHIP_PREFIX = """            if (wl >= base && wl < base + WORDS_PER_LANE) {"""

REC_DECL_START = "    int rec_k_lo = MAX_REC, rec_k_hi = 0;"
REC_DECL_END = "    }\n\n    const int steps ="
REC_LOOP_START = "        for (int k = rec_k_lo; k < rec_k_hi; ++k) {"
REC_LOOP_END = "        }\n        // only the two boundary words cross lanes"

# The lookup-table form this replaced: three MAX_REC arrays indexed by a runtime
# m, plus a dynamic index into the hot register array r. Kept as a variant so
# the cost of the arrays is priced rather than asserted.
ARRAY_FORM_DECL = """    int rec_k[MAX_REC], rec_slot[MAX_REC], rec_bit[MAX_REC];
    int n_mine = 0;
    if (rec_out != nullptr) {
        for (int k = 0; k < n_rec && k < MAX_REC; ++k) {
            int64_t cell = rec_lo_cell + k;
            int64_t wl = (cell >> 5) - tile_start;
            if (wl >= HALO_WORDS && wl < HALO_WORDS + USEFUL_WORDS &&
                wl >= base && wl < base + WORDS_PER_LANE) {
                rec_k[n_mine]    = k;
                rec_slot[n_mine] = (int)(wl - base);
                rec_bit[n_mine]  = (int)(cell & 31);
                ++n_mine;
            }
        }
    }
"""
ARRAY_FORM_LOOP = """        for (int m = 0; m < n_mine; ++m) {
            uint32_t word = r[rec_slot[m]];
            if ((word >> rec_bit[m]) & 1u) {
                atomicOr(&rec_out[rec_k[m] * words_per_batch + (step >> 5)],
                         1u << (step & 31));
            }
        }
"""


def variant(src: str, name: str) -> str:
    """Source surgery, with every edit asserted to have applied."""
    if name == "fixed":
        return src
    if name == "prefix_ownership":
        assert src.count(OWNERSHIP_FIXED) == 1, "ownership block not found once"
        return src.replace(OWNERSHIP_FIXED, OWNERSHIP_PREFIX)
    if name == "array_form":
        # Put back the three MAX_REC lookup arrays and the dynamic index into r.
        i = src.index(REC_DECL_START)
        j = src.index(REC_DECL_END, i)
        out = src[:i] + ARRAY_FORM_DECL + src[j + len("    }\n"):]
        a = out.index(REC_LOOP_START)
        b = out.index(REC_LOOP_END, a)
        out = out[:a] + ARRAY_FORM_LOOP + out[b + len("        }\n"):]
        assert "r[rec_slot[m]]" in out and "if (j == slot)" not in out
        assert "rec_k_lo" not in out.split("extern \"C\"")[1], "range form survived"
        return out
    if name == "no_recording":
        i = src.index(REC_DECL_START)
        j = src.index(REC_DECL_END, i)
        src2 = src[:i] + src[j + len("    }\n"):]
        a = src2.index(REC_LOOP_START)
        b = src2.index(REC_LOOP_END, a)
        src3 = src2[:a] + src2[b + len("        }\n"):]
        # Check for CODE, not for the bare identifier: the file's header comment
        # discusses these names, and asserting on the name alone made this fail
        # on prose while the surgery was in fact correct.
        body = src3.split("extern \"C\"")[1]
        for token in ("atomicOr(&rec_out", "rec_k_lo", "if (j == slot)"):
            assert token not in body, f"recording code survived removal: {token}"
        return src3
    raise ValueError(name)


@app.function(gpu="H100", timeout=1800)
def ablate(bench_words: int = 1 << 22):
    import time, json
    import numpy as np
    import cupy as cp

    src = open("/root/rule30_kernel_v6.cu").read()
    results = []
    # the production config, plus the sweep's fastest
    configs = [(16, 16, 4), (4, 4, 4)]

    for R, H, warps in configs:
        for name in ("fixed", "array_form", "prefix_ownership",
                     "no_recording"):
            code = variant(src, name)
            threads = warps * 32
            spt = 32 * H
            useful = 32 * R - 2 * H
            useful_per_block = useful * warps
            rec = {"variant": name, "words_per_lane": R, "halo_words": H,
                   "warps_per_block": warps}
            opts = (f"-DWORDS_PER_LANE={R}", f"-DHALO_WORDS={H}",
                    f"-DWARPS_PER_BLOCK={warps}", "-DMAX_REC=16", "-std=c++14")
            mod = cp.RawModule(code=code, options=opts, backend="nvcc")
            k = mod.get_function("rule30_v6")
            rec["num_regs"] = int(k.num_regs)
            rec["local_size_bytes"] = int(k.local_size_bytes)
            rec["max_threads_per_block"] = int(k.max_threads_per_block)

            a = cp.random.randint(0, 2**32, size=bench_words, dtype=cp.uint32)
            b = cp.zeros_like(a)
            grid = (bench_words + useful_per_block - 1) // useful_per_block
            args = (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
                    None, np.int32(spt), np.int64(0), np.int32(0))
            nbatch = 8
            for _ in range(2):
                k((grid,), (threads,), args)
            cp.cuda.Stream.null.synchronize()
            t0 = time.time()
            for _ in range(nbatch):
                k((grid,), (threads,),
                  (a, b, np.uint64(bench_words), np.int64(-1), np.int32(0),
                   None, np.int32(spt), np.int64(0), np.int32(0)))
                a, b = b, a
            cp.cuda.Stream.null.synchronize()
            dt = time.time() - t0
            rec["cellsteps_per_s"] = bench_words * 32 * nbatch * spt / dt
            results.append(rec)
            print(f"{R:>3} {H:>3} {warps:>2}  {name:<17} "
                  f"{rec['cellsteps_per_s']:.4e}  regs={rec['num_regs']:>3} "
                  f"local={rec['local_size_bytes']:>4}B", flush=True)

    out = {"results": results}
    # price the fix and the recording code separately, per config
    for R, H, w in configs:
        sel = {r["variant"]: r["cellsteps_per_s"] for r in results
               if (r["words_per_lane"], r["halo_words"],
                   r["warps_per_block"]) == (R, H, w)}
        out[f"ratios_R{R}_H{H}_W{w}"] = {
            # >1 would mean the ownership fix costs throughput
            "fix_cost_x": sel["prefix_ownership"] / sel["fixed"],
            # what remains on the table vs no recording at all
            "recording_code_cost_x": sel["no_recording"] / sel["fixed"],
            # what dropping the three MAX_REC lookup arrays bought
            "range_form_gain_x": sel["fixed"] / sel["array_form"],
        }
    print(json.dumps({k: v for k, v in out.items() if k != "results"}, indent=2))
    return out


@app.local_entrypoint()
def main():
    import json
    res = ablate.remote()
    with open("ablate_v6_result.json", "w") as f:
        json.dump(res, f, indent=2)
