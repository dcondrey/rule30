//! Candidate implementations of `solve(n) -> a(n)`, the nth bit of the rule 30
//! center column (OEIS A051023, offset 0). One is selected per build via a
//! feature so each ships as its own WASM artifact.

#[cfg(feature = "naive")]
#[unsafe(no_mangle)]
pub extern "C" fn solve(n: i64) -> i64 {
    if n < 0 {
        return -1;
    }
    let n = n as usize;
    let width = 2 * n + 5;
    let centre = n + 2;
    let mut cur = vec![0u8; width];
    let mut next = vec![0u8; width];
    cur[centre] = 1;
    for _ in 0..n {
        for i in 1..width - 1 {
            next[i] = cur[i - 1] ^ (cur[i] | cur[i + 1]);
        }
        core::mem::swap(&mut cur, &mut next);
    }
    cur[centre] as i64
}

#[cfg(feature = "bitparallel")]
#[unsafe(no_mangle)]
pub extern "C" fn solve(n: i64) -> i64 {
    if n < 0 {
        return -1;
    }
    let n = n as usize;
    let words = (2 * n + 5 + 63) / 64 + 1;
    let centre = n + 2;
    let mut cur = vec![0u64; words];
    let mut next = vec![0u64; words];
    cur[centre / 64] = 1u64 << (centre % 64);
    for _ in 0..n {
        for i in 0..words {
            let c = cur[i];
            // bit b of `cur[i]` is the cell at position 64*i + b, so the left
            // neighbour arrives as a left shift and the right as a right shift.
            let l = (c << 1) | if i > 0 { cur[i - 1] >> 63 } else { 0 };
            let r = (c >> 1) | if i + 1 < words { cur[i + 1] << 63 } else { 0 };
            next[i] = l ^ (c | r);
        }
        core::mem::swap(&mut cur, &mut next);
    }
    ((cur[centre / 64] >> (centre % 64)) & 1) as i64
}

#[cfg(feature = "constant")]
#[unsafe(no_mangle)]
pub extern "C" fn solve(_n: i64) -> i64 {
    1
}
