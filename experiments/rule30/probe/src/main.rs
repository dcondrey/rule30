//! Rule 30 = Rule 150 + sparse error term. Steps 1 and 2 of the superposition
//! build order: the error-event probe and the Rule 150 projector.
//!
//! Convention matches `experiments/rule30/center_column.py`:
//!   new = (row<<1) ^ (row | (row>>1))
//! bit p holds cell p, position increasing rightward, so the left neighbour of
//! p is p-1 and the right neighbour is p+1.
//!
//!   f30(l,c,r) = l ^ (c | r) = l ^ c ^ r ^ (c & r) = f150(l,c,r) ^ E
//!   E(x,t)     = s_t(x) & s_t(x+1)
//!
//! With A = x + 1 + x^-1 the Rule 150 operator over GF(2):
//!   s_n = A^n s_0 + sum_{t<n} A^{n-1-t} e_t
//! and the center cell picks out
//!   [A^d delta_x]_0 = coeff of z^(|x|+d) in (1+z+z^2)^d.

use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::time::Instant;

const W: usize = 64;

// ---------------------------------------------------------------- bit vectors

fn shl_into(src: &[u64], k: usize, dst: &mut [u64]) {
    let wo = k / W;
    let bo = k % W;
    for j in (0..dst.len()).rev() {
        let mut v = 0u64;
        if j >= wo && j - wo < src.len() {
            v = src[j - wo] << bo;
        }
        if bo > 0 && j > wo && j - wo - 1 < src.len() {
            v |= src[j - wo - 1] >> (W - bo);
        }
        dst[j] = v;
    }
}

fn shr1_into(src: &[u64], dst: &mut [u64]) {
    let n = src.len();
    for j in 0..n {
        let mut v = src[j] >> 1;
        if j + 1 < n {
            v |= src[j + 1] << (W - 1);
        }
        dst[j] = v;
    }
}

fn shl1_into(src: &[u64], dst: &mut [u64]) {
    for j in (0..src.len()).rev() {
        let mut v = src[j] << 1;
        if j > 0 {
            v |= src[j - 1] >> (W - 1);
        }
        dst[j] = v;
    }
}

fn get(b: &[u64], i: usize) -> bool {
    (b[i / W] >> (i % W)) & 1 == 1
}

fn popcount(b: &[u64]) -> u64 {
    b.iter().map(|w| w.count_ones() as u64).sum()
}

// ------------------------------------------------- step 2: the Lucas projector

/// Parity of the coefficient of z^k in (1+z+z^2)^d over GF(2).
///
/// Over GF(2), (1+z+z^2)^(2^m) = 1 + z^(2^m) + z^(2^(m+1)), so the polynomial
/// factors as a product over the set bits of `d`. Choosing exponent
/// c_m * 2^m with c_m in {0,1,2} from factor m, the coefficient counts the
/// solutions of sum c_m 2^m = k, mod 2. A carry DP over the bits of k does
/// that in O(bits) with carry confined to {0,1}.
///
/// Lucas' theorem is the popcount-mask special case for the *binomial*
/// (1+z)^d, i.e. Rule 90. The trinomial needs this DP; it is not Lucas.
fn trinom_mod2(d: u64, k: u64) -> u8 {
    // cnt[c] = parity of the number of partial assignments leaving carry c.
    let mut cnt = [1u8, 0u8];
    for m in 0..64 {
        let kbit = ((k >> m) & 1) as u64;
        let dbit = (d >> m) & 1;
        let mut next = [0u8, 0u8];
        for c in 0..2u64 {
            if cnt[c as usize] == 0 {
                continue;
            }
            let hi = if dbit == 1 { 2 } else { 0 };
            for choice in 0..=hi {
                let total = choice + c;
                if total & 1 != kbit {
                    continue;
                }
                next[(total >> 1) as usize] ^= cnt[c as usize];
            }
        }
        cnt = next;
        if cnt == [0, 0] {
            return 0;
        }
    }
    cnt[0]
}

/// Does the error event at (x, t) flip the center cell at step n?
///
/// x is signed, relative to the initial single 1 at x = 0. The event is
/// produced from row t and enters row t+1 as a delta at position x, so it is
/// carried by A^(n-1-t).
fn projects_to_center(x: i64, t: u64, n: u64) -> bool {
    if t + 1 > n {
        return false;
    }
    let d = n - 1 - t;
    let a = x.unsigned_abs();
    if a > d {
        return false;
    }
    trinom_mod2(d, a + d) == 1
}

/// Rule 150 center cell at step n from a single 1: coeff of z^n in (1+z+z^2)^n.
fn rule150_center(n: u64) -> u8 {
    trinom_mod2(n, n)
}

// ------------------------------------ bulk path: full (1+z+z^2)^d coefficients

/// Writes the coefficients of (1+z+z^2)^d into `buf` (must hold 2d+1 bits).
fn trinom_poly(d: u64, buf: &mut Vec<u64>, t1: &mut Vec<u64>, t2: &mut Vec<u64>) {
    let bits = (2 * d + 1) as usize;
    let words = bits.div_ceil(W);
    buf.clear();
    buf.resize(words, 0);
    t1.clear();
    t1.resize(words, 0);
    t2.clear();
    t2.resize(words, 0);
    buf[0] = 1;
    for m in 0..64 {
        if (d >> m) & 1 == 0 {
            continue;
        }
        let a = 1usize << m;
        shl_into(buf, a, t1);
        shl_into(buf, 2 * a, t2);
        for j in 0..words {
            buf[j] ^= t1[j] ^ t2[j];
        }
    }
}

/// popcount( err & (poly << shift) ) without materialising the shifted poly.
fn shifted_and_count(err: &[u64], poly: &[u64], shift: usize) -> u64 {
    let wo = shift / W;
    let bo = shift % W;
    let mut acc = 0u64;
    for (i, &p) in poly.iter().enumerate() {
        if p == 0 {
            continue;
        }
        let j = i + wo;
        if j < err.len() {
            acc += (err[j] & (p << bo)).count_ones() as u64;
        }
        if bo > 0 && j + 1 < err.len() {
            acc += (err[j + 1] & (p >> (W - bo))).count_ones() as u64;
        }
    }
    acc
}

// ------------------------------------------------ step 1: the baseline probe

struct Probe {
    off: usize,
    words: usize,
    /// err[t] = error bitmap of row t, bit (x+off) set iff E(x,t)=1.
    err: Vec<Vec<u64>>,
    /// center[t] = Rule 30 center cell at step t (t=0 is the seed row).
    center: Vec<u8>,
}

fn simulate(max_n: usize) -> Probe {
    let off = max_n + 2;
    let bits = 2 * max_n + 8;
    let words = bits.div_ceil(W);
    let mut row = vec![0u64; words];
    row[off / W] |= 1 << (off % W);
    let mut a = vec![0u64; words];
    let mut b = vec![0u64; words];
    let mut err = Vec::with_capacity(max_n);
    let mut center = Vec::with_capacity(max_n + 1);
    for _ in 0..max_n {
        center.push(get(&row, off) as u8);
        shr1_into(&row, &mut b);
        let mut e = vec![0u64; words];
        for j in 0..words {
            e[j] = row[j] & b[j];
        }
        err.push(e);
        shl1_into(&row, &mut a);
        for j in 0..words {
            row[j] = a[j] ^ (row[j] | b[j]);
        }
    }
    center.push(get(&row, off) as u8);
    Probe { off, words, err, center }
}

impl Probe {
    /// (count, parity) of error events that project onto the center at step n.
    fn project(&self, n: usize, per_row: Option<&mut Vec<u64>>) -> (u64, u8) {
        let mut buf = Vec::new();
        let mut t1 = Vec::new();
        let mut t2 = Vec::new();
        let mut total = 0u64;
        let mut rows = per_row;
        for t in 0..n {
            let d = (n - 1 - t) as u64;
            trinom_poly(d, &mut buf, &mut t1, &mut t2);
            let shift = self.off - d as usize;
            let c = shifted_and_count(&self.err[t], &buf, shift);
            if let Some(r) = rows.as_deref_mut() {
                r.push(c);
            }
            total += c;
        }
        (total, (total & 1) as u8)
    }
}

// ------------------------------------------- step 3: parity cancellation

/// Row parity of the projected error set, and its dyadic block structure.
///
/// `Probe::project` already returns the per-row count of events surviving the
/// kernel, so a row's parity is that count mod 2 and a block's parity is the XOR
/// of its rows. The block covering all n rows is therefore the center-cell
/// correction that verify-3 pins, which makes the last histogram line a check.
fn parity_report(p: &Probe, n: usize) {
    let mut rows = Vec::with_capacity(n);
    let t0 = Instant::now();
    let (total, parity) = p.project(n, Some(&mut rows));
    let row_parities: Vec<u8> = rows.iter().map(|&c| (c & 1) as u8).collect();
    let non_zero_rows = row_parities.iter().filter(|&&q| q != 0).count();

    println!();
    println!("## parity cancellation at n = {n}");
    println!(
        "n={}: {} non-zero rows out of {} ({:.2}% survival)  [N_eff={} in {:?}]",
        n,
        non_zero_rows,
        n,
        (non_zero_rows as f64 / n as f64) * 100.0,
        total,
        t0.elapsed()
    );
    println!(
        "row-survival exponent: log2({}) / log2({}) = {:.4}  (= 1 - log2(1/frac)/log2(n); it converges to 1, it is not sublinear -- read the grid fit instead)",
        non_zero_rows,
        n,
        (non_zero_rows as f64).log2() / (n as f64).log2()
    );

    println!();
    println!("### row-parity survival by decile of t");
    println!("  t-range          rows    non-zero   fraction");
    let dec = n / 10;
    for i in 0..10 {
        let lo = i * dec;
        let hi = if i == 9 { n } else { (i + 1) * dec };
        let nz = row_parities[lo..hi].iter().filter(|&&q| q != 0).count();
        println!(
            "{lo:>6}..{hi:<6} {:>8} {:>11}   {:.5}",
            hi - lo,
            nz,
            nz as f64 / (hi - lo) as f64
        );
    }

    println!();
    println!("### dyadic block cancellation");
    println!("block_size   non-zero / total     fraction   exponent   (total < 16 blocks: too few samples to read)");
    let mut block_size = 1usize;
    while block_size <= n {
        let mut non_zero_blocks = 0usize;
        let mut total_blocks = 0usize;
        for chunk in row_parities.chunks(block_size) {
            let block_parity = chunk.iter().fold(0u8, |acc, &q| acc ^ q);
            if block_parity != 0 {
                non_zero_blocks += 1;
            }
            total_blocks += 1;
        }
        let expo = if non_zero_blocks > 0 {
            (non_zero_blocks as f64).log2() / (n as f64).log2()
        } else {
            0.0
        };
        println!(
            "{block_size:>10}   {non_zero_blocks:>8} / {total_blocks:<8}   {:>8.5}   {expo:>8.4}",
            non_zero_blocks as f64 / total_blocks as f64
        );
        block_size *= 2;
    }
    let all: u8 = row_parities.iter().fold(0u8, |acc, &q| acc ^ q);
    assert_eq!(all, parity, "block-XOR disagrees with projected parity at n={n}");
}

// ------------------------------------------------------------------- reporting

fn main() {
    let mut args = std::env::args().skip(1);
    let max_n: usize = args.next().and_then(|s| s.parse().ok()).unwrap_or(10_000);
    let mut parity_targets: Vec<usize> = args.filter_map(|s| s.parse().ok()).collect();
    if parity_targets.is_empty() {
        parity_targets = vec![4045, 8113];
    }
    parity_targets.retain(|&n| n >= 1 && n <= max_n);
    parity_targets.sort_unstable();
    parity_targets.dedup();

    println!("# rule 30 superposition probe: max_n = {max_n}");
    println!();

    let t0 = Instant::now();
    let p = simulate(max_n);
    println!("[sim] {max_n} rows in {:?} ({} words/row)", t0.elapsed(), p.words);

    // ---- verification 1: DP projector vs full-polynomial expansion
    let mut buf = Vec::new();
    let mut t1 = Vec::new();
    let mut t2 = Vec::new();
    let mut checked = 0u64;
    let mut ds: Vec<u64> = (0..=300).collect();
    for m in 0..13u32 {
        for delta in [-1i64, 0, 1] {
            let v = (1i64 << m) + delta;
            if v >= 0 && v <= max_n as i64 {
                ds.push(v as u64);
            }
        }
    }
    ds.push(max_n as u64 - 1);
    ds.sort_unstable();
    ds.dedup();
    for &d in &ds {
        trinom_poly(d, &mut buf, &mut t1, &mut t2);
        for k in 0..=(2 * d) {
            let a = trinom_mod2(d, k);
            let b = get(&buf, k as usize) as u8;
            assert_eq!(a, b, "trinom mismatch d={d} k={k}");
            checked += 1;
        }
        assert_eq!(trinom_mod2(d, 2 * d + 1), 0, "support overrun d={d}");
    }
    println!("[verify-1] DP == polynomial expansion over {checked} coefficients, {} values of d (max {})", ds.len(), ds.last().unwrap());

    // ---- verification 2: rule150_center vs a direct Rule 150 simulation
    {
        let n150 = 4096usize.min(max_n);
        let off = n150 + 2;
        let words = (2 * n150 + 8).div_ceil(W);
        let mut row = vec![0u64; words];
        row[off / W] |= 1 << (off % W);
        let mut a = vec![0u64; words];
        let mut b = vec![0u64; words];
        for t in 0..n150 {
            assert_eq!(get(&row, off) as u8, rule150_center(t as u64), "rule150 center mismatch t={t}");
            shl1_into(&row, &mut a);
            shr1_into(&row, &mut b);
            for j in 0..words {
                row[j] ^= a[j] ^ b[j];
            }
        }
        println!("[verify-2] rule150_center(n) == direct rule 150 simulation for n in 0..{n150}");
    }

    // ---- verification 3: the superposition identity itself
    let exhaustive = 512usize.min(max_n);
    for n in 1..=exhaustive {
        let (_, parity) = p.project(n, None);
        let pred = rule150_center(n as u64) ^ parity;
        assert_eq!(pred, p.center[n], "identity mismatch n={n}");
    }
    let mut bands: Vec<usize> = Vec::new();
    for base in [1000usize, 2000, 4000] {
        if base + 64 <= max_n {
            bands.extend(base..base + 64);
        }
    }
    for m in 9..15u32 {
        for delta in [-1i64, 0, 1] {
            let v = (1i64 << m) + delta;
            if v >= 1 && v <= max_n as i64 {
                bands.push(v as usize);
            }
        }
    }
    if max_n >= 1 {
        bands.push(max_n);
    }
    bands.sort_unstable();
    bands.dedup();
    for &n in &bands {
        let (_, parity) = p.project(n, None);
        let pred = rule150_center(n as u64) ^ parity;
        assert_eq!(pred, p.center[n], "identity mismatch n={n}");
    }
    println!(
        "[verify-3] s_n(0) == rule150_center(n) XOR parity(projected errors) for all n in 1..={exhaustive} and {} banded n (max {})",
        bands.len(),
        bands.last().unwrap()
    );
    println!();

    // ---- geometry of the raw error set
    let mut row_count = vec![0u64; max_n];
    let mut h_left = [0u64; 65];
    let mut h_right = [0u64; 65];
    let mut h_center = [0u64; 65];
    let mut total_err = 0u64;
    for t in 0..max_n {
        let c = popcount(&p.err[t]);
        row_count[t] = c;
        total_err += c;
        let lo = p.off as i64 - t as i64;
        let hi = p.off as i64 + t as i64;
        for i in lo..=hi {
            if !get(&p.err[t], i as usize) {
                continue;
            }
            let x = i - p.off as i64;
            let dl = (x + t as i64) as usize;
            let dr = (t as i64 - x) as usize;
            let dc = x.unsigned_abs() as usize;
            h_left[dl.min(64)] += 1;
            h_right[dr.min(64)] += 1;
            h_center[dc.min(64)] += 1;
        }
    }
    let cone_cells: u64 = (0..max_n as u64).map(|t| 2 * t + 1).sum();
    println!("## raw error events E(x,t)=1");
    println!("total = {total_err} over {cone_cells} light-cone cells  density = {:.6}", total_err as f64 / cone_cells as f64);
    let tail: u64 = row_count[max_n / 2..].iter().sum();
    let tail_cells: u64 = (max_n as u64 / 2..max_n as u64).map(|t| 2 * t + 1).sum();
    println!("bulk density (t >= {}) = {:.6}", max_n / 2, tail as f64 / tail_cells as f64);
    println!();
    println!("### distance-from-edge histograms (all t, counts / cells at that depth)");
    println!("  d   from-left-edge      from-right-edge     from-center");
    for d in 0..24usize {
        let cells = (max_n - d.min(max_n)) as f64;
        let cells_c = (max_n as i64 - d as i64).max(0) as f64;
        println!(
            "{d:>3}   {:>10} {:.4}   {:>10} {:.4}   {:>10} {:.4}",
            h_left[d], h_left[d] as f64 / cells,
            h_right[d], h_right[d] as f64 / cells,
            h_center[d], h_center[d] as f64 / (2.0 * cells_c.max(1.0))
        );
    }
    println!();

    // ---- the number that decides the arm
    println!("## effective errors: |{{(x,t) : E(x,t)=1 AND projects_to_center(x,t,n)}}|");
    println!("     n    cone_cells      raw_E   effective    eff/raw   eff/n^2   log2(eff)/log2(n)  center");
    // Power-of-two targets alias with the popcount structure of the kernel
    // d = n-1-t, so the sweep is a geometric grid deliberately off that lattice.
    // The aligned points are kept, flagged, and excluded from the fit.
    let mut targets: Vec<usize> = Vec::new();
    let mut aligned: Vec<usize> = Vec::new();
    let mut v = 200.0f64;
    while (v as usize) <= max_n {
        targets.push(v as usize);
        v *= 1.15;
    }
    for m in 6..=13u32 {
        let p = 1usize << m;
        if p <= max_n {
            aligned.push(p);
        }
    }
    for &p in &aligned {
        targets.push(p);
    }
    if max_n >= 1 {
        targets.push(max_n);
    }
    targets.sort_unstable();
    targets.dedup();
    let mut fit_pts: Vec<(f64, f64)> = Vec::new();
    let mut per_row_dump: BTreeMap<usize, Vec<u64>> = BTreeMap::new();
    for &n in &targets {
        let mut rows = Vec::with_capacity(n);
        let t = Instant::now();
        let (eff, parity) = p.project(n, Some(&mut rows));
        let raw: u64 = row_count[..n].iter().sum();
        let cells: u64 = (0..n as u64).map(|t| 2 * t + 1).sum();
        let pred = rule150_center(n as u64) ^ parity;
        assert_eq!(pred, p.center[n], "identity mismatch n={n}");
        println!(
            "{n:>6}  {cells:>12} {raw:>10} {eff:>11}   {:.5}   {:.6}   {:>10.4}          {pred}  [{:?}]",
            eff as f64 / raw as f64,
            eff as f64 / (n as f64 * n as f64),
            (eff as f64).log2() / (n as f64).log2(),
            t.elapsed()
        );
        if eff > 0 && !aligned.contains(&n) {
            fit_pts.push(((n as f64).ln(), (eff as f64).ln()));
        }
        if n == *targets.last().unwrap() {
            per_row_dump.insert(n, rows);
        }
    }

    // log-log slope over the upper half of the sweep
    if fit_pts.len() >= 3 {
        let half = &fit_pts[fit_pts.len() / 2..];
        let k = half.len() as f64;
        let sx: f64 = half.iter().map(|p| p.0).sum();
        let sy: f64 = half.iter().map(|p| p.1).sum();
        let sxx: f64 = half.iter().map(|p| p.0 * p.0).sum();
        let sxy: f64 = half.iter().map(|p| p.0 * p.1).sum();
        let slope = (k * sxy - sx * sy) / (k * sxx - sx * sx);
        let icpt = (sy - slope * sx) / k;
        println!();
        println!("[fit] log(effective) = {slope:.4} * log(n) + {icpt:.4}   over the upper half of the sweep");
    }

    // ---- where the surviving errors live, for the largest target
    if let Some((&n, rows)) = per_row_dump.iter().next() {
        println!();
        println!("## per-row effective count at n = {n} (decile summary of t)");
        println!("  t-range          rows   eff_count    eff/row    raw/row   survival");
        let dec = n / 10;
        for i in 0..10 {
            let lo = i * dec;
            let hi = if i == 9 { n } else { (i + 1) * dec };
            let e: u64 = rows[lo..hi].iter().sum();
            let r: u64 = row_count[lo..hi].iter().sum();
            println!(
                "{lo:>6}..{hi:<6} {:>8} {:>11} {:>10.2} {:>10.2}   {:.5}",
                hi - lo, e,
                e as f64 / (hi - lo) as f64,
                r as f64 / (hi - lo) as f64,
                if r > 0 { e as f64 / r as f64 } else { 0.0 }
            );
        }
    }

    // ---- row-parity survival across the whole grid
    println!();
    println!("## row-parity survival across the 1.15^k grid");
    println!("the log(nz)/log(n) column rises toward 1 purely because the 1/2 constant decays; the fit below is the statistic");
    println!("     n   non-zero rows   fraction   log(nz)/log(n)   aligned");
    let mut par_fit: Vec<(f64, f64)> = Vec::new();
    for &n in &targets {
        let mut rows = Vec::with_capacity(n);
        let _ = p.project(n, Some(&mut rows));
        let nz = rows.iter().filter(|&&c| c & 1 == 1).count();
        let al = aligned.contains(&n);
        println!(
            "{n:>6}   {nz:>13}   {:>8.5}   {:>14.4}   {}",
            nz as f64 / n as f64,
            if nz > 0 { (nz as f64).log2() / (n as f64).log2() } else { 0.0 },
            if al { "yes" } else { "" }
        );
        if nz > 0 && !al {
            par_fit.push(((n as f64).ln(), (nz as f64).ln()));
        }
    }
    if par_fit.len() >= 3 {
        let half = &par_fit[par_fit.len() / 2..];
        let k = half.len() as f64;
        let sx: f64 = half.iter().map(|q| q.0).sum();
        let sy: f64 = half.iter().map(|q| q.1).sum();
        let sxx: f64 = half.iter().map(|q| q.0 * q.0).sum();
        let sxy: f64 = half.iter().map(|q| q.0 * q.1).sum();
        let slope = (k * sxy - sx * sy) / (k * sxx - sx * sx);
        let icpt = (sy - slope * sx) / k;
        println!();
        println!("[fit] log(non-zero rows) = {slope:.4} * log(n) + {icpt:.4}   over the upper half of the sweep ({} pts)", half.len());
    }

    // ---- parity cancellation on the unaligned targets
    for &n in &parity_targets {
        parity_report(&p, n);
    }

    // ---- projector cost
    println!();
    let mut sink = 0u64;
    let iters = 2_000_000u64;
    let t = Instant::now();
    for i in 0..iters {
        let n = max_n as u64;
        let tt = i % n;
        let x = (i as i64 % (2 * tt as i64 + 1)) - tt as i64;
        sink += projects_to_center(x, tt, n) as u64;
    }
    let el = t.elapsed();
    println!("## projector cost");
    println!(
        "projects_to_center: {iters} calls in {:?} = {:.1} ns/call (sink={sink})",
        el,
        el.as_nanos() as f64 / iters as f64
    );
    println!("DP is O(bits(n)) carry steps, not O(1); at n={max_n} that is {} iterations worst case", 64 - (max_n as u64).leading_zeros());

    // ---- raw coordinate dump for n <= 1024
    let dump_n = 1024usize.min(max_n);
    let mut s = String::new();
    let _ = writeln!(s, "t,x");
    for t in 0..dump_n {
        let lo = p.off as i64 - t as i64;
        let hi = p.off as i64 + t as i64;
        for i in lo..=hi {
            if get(&p.err[t], i as usize) {
                let _ = writeln!(s, "{t},{}", i - p.off as i64);
            }
        }
    }
    let path = concat!(env!("CARGO_MANIFEST_DIR"), "/../errors-le1024.csv");
    std::fs::write(path, s).expect("write dump");
    println!();
    println!("[dump] raw (t,x) error coordinates for t < {dump_n} -> experiments/rule30/errors-le1024.csv");
}
