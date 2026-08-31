//! GPU centre-column generator for Rule 30, lone seed.
//!
//! Architecture is the standard one: ping-pong storage buffers that never leave
//! VRAM, a packed history buffer written by the single invocation that owns the
//! centre word, and a MAP_READ staging buffer drained once per batch.
//!
//! Three corrections relative to the naive form, each load-bearing:
//!
//! 1. Neighbour shifts. With cell `32*i + j` in bit `j` of word `i`, the LEFT
//!    neighbour word is `(c << 1) | (left >> 31)` and the RIGHT neighbour word
//!    is `(c >> 1) | (right << 31)`. Swapping these produces a wrong row at the
//!    very first step.
//!
//! 2. Lattice width. The centre cell at time `t` depends on cells `[-t, t]`, so
//!    a fixed-width array of `W` cells yields correct centre bits only while
//!    `t <= W/2 - 1`. Past that the zero boundary is no longer the true
//!    infinite-lattice evolution and every later bit is silently wrong. We size
//!    the lattice from the requested depth and assert the margin.
//!
//! 3. History index is batch-local (`step % BATCH`), not the global generation.
//!    A global index walks off the end of the history buffer after one batch.
//!
//! `atomicOr` packing is used as specified: 32x smaller history, and the buffer
//! is cleared before every batch because OR can only set bits.

use std::time::Instant;
use wgpu::util::DeviceExt;

const WORKGROUP: u32 = 256;
/// Generations per submit. Also the number of bits packed per history batch.
const BATCH: u32 = 8192;
/// Dynamic uniform offsets must be 256-byte aligned.
const UNIFORM_STRIDE: u64 = 256;

const SHADER: &str = r#"
struct Step { step: u32, _p0: u32, _p1: u32, _p2: u32 };

@group(0) @binding(0) var<storage, read>       cur:     array<u32>;
@group(0) @binding(1) var<storage, read_write> next:    array<u32>;
@group(0) @binding(2) var<storage, read_write> history: array<atomic<u32>>;
@group(0) @binding(3) var<uniform>             s:       Step;
@group(0) @binding(4) var<uniform>             cone:    Step;   // .step = lo word, ._p0 = hi word

override CENTER_WORD: u32;
override CENTER_BIT:  u32;

@compute @workgroup_size(256)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    // Active-cone dispatch: only words the light cone can have reached.
    let i = cone.step + gid.x;
    let n = arrayLength(&cur);
    if (i >= n || i > cone._p0) { return; }

    let c = cur[i];
    var lw = 0u;
    var rw = 0u;
    if (i > 0u)      { lw = cur[i - 1u]; }
    if (i + 1u < n)  { rw = cur[i + 1u]; }

    // cell 32*i+j lives in bit j, so the left neighbour of bit j is bit j-1.
    let l = (c << 1u) | (lw >> 31u);
    let r = (c >> 1u) | (rw << 31u);

    next[i] = l ^ (c | r);

    // One invocation owns the centre word and logs the pre-update centre bit.
    if (i == CENTER_WORD) {
        let bit = (c >> CENTER_BIT) & 1u;
        atomicOr(&history[s.step / 32u], bit << (s.step % 32u));
    }
}
"#;

/// CPU reference, identical recurrence to experiments/rule30/center_column.py.
fn cpu_center_column(steps: usize) -> Vec<u8> {
    let off = steps + 2;
    let mut row = num_bigint_shim::One::one_shl(off);
    let mut out = Vec::with_capacity(steps);
    for _ in 0..steps {
        out.push(row.bit(off));
        row = row.step30();
    }
    out
}

/// Minimal big-unsigned helper so the reference needs no extra dependency.
mod num_bigint_shim {
    #[derive(Clone)]
    pub struct One {
        limbs: Vec<u64>,
    }
    impl One {
        pub fn one_shl(n: usize) -> One {
            let mut limbs = vec![0u64; n / 64 + 2];
            limbs[n / 64] = 1u64 << (n % 64);
            One { limbs }
        }
        pub fn bit(&self, n: usize) -> u8 {
            ((self.limbs[n / 64] >> (n % 64)) & 1) as u8
        }
        fn shl1(&self) -> One {
            let mut out = vec![0u64; self.limbs.len() + 1];
            let mut carry = 0u64;
            for (i, &w) in self.limbs.iter().enumerate() {
                out[i] = (w << 1) | carry;
                carry = w >> 63;
            }
            let n = out.len();
            out[n - 1] = carry;
            One { limbs: out }
        }
        fn shr1(&self) -> One {
            let mut out = vec![0u64; self.limbs.len()];
            for i in 0..self.limbs.len() {
                let hi = if i + 1 < self.limbs.len() { self.limbs[i + 1] } else { 0 };
                out[i] = (self.limbs[i] >> 1) | (hi << 63);
            }
            One { limbs: out }
        }
        /// row' = (row<<1) ^ (row | (row>>1))
        pub fn step30(&self) -> One {
            let l = self.shl1();
            let r = self.shr1();
            let n = l.limbs.len();
            let mut out = vec![0u64; n];
            for i in 0..n {
                let s = if i < self.limbs.len() { self.limbs[i] } else { 0 };
                let rr = if i < r.limbs.len() { r.limbs[i] } else { 0 };
                out[i] = l.limbs[i] ^ (s | rr);
            }
            One { limbs: out }
        }
    }
}

async fn run(depth: u32, verify: usize) {
    // --- lattice sizing: centre at time t needs cells [-t, t] ---------------
    let need_cells = 2 * depth as u64 + 64;
    let words = ((need_cells + 31) / 32).next_multiple_of(WORKGROUP as u64) as u32;
    let center_word = words / 2;
    let center_bit = 0u32;
    // Distance in cells from the seed to the nearest lattice edge.
    let margin = (center_word as u64) * 32;
    assert!(
        margin > depth as u64,
        "lattice too narrow: margin {margin} cells cannot support depth {depth}"
    );

    let instance = wgpu::Instance::default();
    let adapter = instance
        .request_adapter(&wgpu::RequestAdapterOptions::default())
        .await
        .expect("no GPU adapter");
    let (device, queue) = adapter
        .request_device(&wgpu::DeviceDescriptor {
            label: None,
            required_features: wgpu::Features::empty(),
            required_limits: wgpu::Limits {
                max_storage_buffer_binding_size: u32::MAX / 2,
                max_buffer_size: 1 << 32,
                ..wgpu::Limits::default()
            },
            memory_hints: Default::default(),
            trace: wgpu::Trace::Off,
        })
        .await
        .expect("no device");

    let info = adapter.get_info();
    println!(
        "GPU: {} ({:?}, {:?})\nlattice: {} words = {} cells, centre word {}, margin {} cells",
        info.name, info.backend, info.device_type, words, words as u64 * 32, center_word, margin
    );

    // --- buffers -------------------------------------------------------------
    let bytes = words as u64 * 4;
    let mut init = vec![0u32; words as usize];
    init[center_word as usize] = 1 << center_bit;

    let buf_a = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("A"),
        contents: bytemuck::cast_slice(&init),
        usage: wgpu::BufferUsages::STORAGE,
    });
    let buf_b = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("B"),
        size: bytes,
        usage: wgpu::BufferUsages::STORAGE,
        mapped_at_creation: false,
    });

    let hist_bytes = (BATCH as u64 / 32) * 4;
    let history = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("history"),
        size: hist_bytes,
        // COPY_DST is required by clear_buffer, which the atomicOr packing
        // depends on: OR can only set bits, so each batch must start zeroed.
        usage: wgpu::BufferUsages::STORAGE
            | wgpu::BufferUsages::COPY_SRC
            | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    let staging = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("staging"),
        size: hist_bytes,
        usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });

    // Pre-filled step indices, one 256-byte aligned slot per dispatch.
    let mut steps = vec![0u8; (BATCH as u64 * UNIFORM_STRIDE) as usize];
    for i in 0..BATCH {
        let o = (i as u64 * UNIFORM_STRIDE) as usize;
        steps[o..o + 4].copy_from_slice(&i.to_le_bytes());
    }
    let cone_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("cone"),
        size: 16,
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    let step_buf = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("steps"),
        contents: &steps,
        usage: wgpu::BufferUsages::UNIFORM,
    });

    // --- pipeline ------------------------------------------------------------
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("rule30"),
        source: wgpu::ShaderSource::Wgsl(SHADER.into()),
    });

    let sto = |ro: bool| wgpu::BindingType::Buffer {
        ty: wgpu::BufferBindingType::Storage { read_only: ro },
        has_dynamic_offset: false,
        min_binding_size: None,
    };
    let layout = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: None,
        entries: &[
            wgpu::BindGroupLayoutEntry { binding: 0, visibility: wgpu::ShaderStages::COMPUTE, ty: sto(true), count: None },
            wgpu::BindGroupLayoutEntry { binding: 1, visibility: wgpu::ShaderStages::COMPUTE, ty: sto(false), count: None },
            wgpu::BindGroupLayoutEntry { binding: 2, visibility: wgpu::ShaderStages::COMPUTE, ty: sto(false), count: None },
            wgpu::BindGroupLayoutEntry {
                binding: 3,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Uniform,
                    has_dynamic_offset: true,
                    min_binding_size: wgpu::BufferSize::new(16),
                },
                count: None,
            },
            wgpu::BindGroupLayoutEntry {
                binding: 4,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Uniform,
                    has_dynamic_offset: false,
                    min_binding_size: wgpu::BufferSize::new(16),
                },
                count: None,
            },
        ],
    });
    let pl = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: None,
        bind_group_layouts: &[&layout],
        push_constant_ranges: &[],
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: None,
        layout: Some(&pl),
        module: &shader,
        entry_point: Some("main"),
        compilation_options: wgpu::PipelineCompilationOptions {
            constants: &[
                ("CENTER_WORD", center_word as f64),
                ("CENTER_BIT", center_bit as f64),
            ],
            ..Default::default()
        },
        cache: None,
    });

    let bg = |cur: &wgpu::Buffer, nxt: &wgpu::Buffer| {
        device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: None,
            layout: &layout,
            entries: &[
                wgpu::BindGroupEntry { binding: 0, resource: cur.as_entire_binding() },
                wgpu::BindGroupEntry { binding: 1, resource: nxt.as_entire_binding() },
                wgpu::BindGroupEntry { binding: 2, resource: history.as_entire_binding() },
                wgpu::BindGroupEntry {
                    binding: 3,
                    resource: wgpu::BindingResource::Buffer(wgpu::BufferBinding {
                        buffer: &step_buf, offset: 0, size: wgpu::BufferSize::new(16),
                    }),
                },
                wgpu::BindGroupEntry { binding: 4, resource: cone_buf.as_entire_binding() },
            ],
        })
    };
    let bg_ab = bg(&buf_a, &buf_b);
    let bg_ba = bg(&buf_b, &buf_a);

    // --- run -----------------------------------------------------------------
    let mut bits: Vec<u8> = Vec::with_capacity(depth as usize);
    let t0 = Instant::now();
    let mut done = 0u32;

    while done < depth {
        let n = BATCH.min(depth - done);

        // The cone at the END of this batch bounds every step within it.
        let half_cells = (done + n) as u64 + 64;
        let half_words = (half_cells / 32 + 2) as u32;
        let lo = center_word.saturating_sub(half_words);
        let hi = (center_word + half_words).min(words - 1);
        let groups = (hi - lo + 1).div_ceil(WORKGROUP);
        queue.write_buffer(&cone_buf, 0, bytemuck::cast_slice(&[lo, hi, 0u32, 0u32]));

        let mut enc = device.create_command_encoder(&Default::default());
        enc.clear_buffer(&history, 0, None); // atomicOr only sets bits
        {
            let mut pass = enc.begin_compute_pass(&Default::default());
            pass.set_pipeline(&pipeline);
            for i in 0..n {
                let parity_even = (done + i) % 2 == 0;
                pass.set_bind_group(
                    0,
                    if parity_even { &bg_ab } else { &bg_ba },
                    &[(i as u64 * UNIFORM_STRIDE) as u32],
                );
                pass.dispatch_workgroups(groups, 1, 1);
            }
        }
        enc.copy_buffer_to_buffer(&history, 0, &staging, 0, hist_bytes);
        queue.submit(Some(enc.finish()));

        let slice = staging.slice(..);
        slice.map_async(wgpu::MapMode::Read, |_| {});
        device.poll(wgpu::PollType::Wait).unwrap();
        {
            let data = slice.get_mapped_range();
            let w: &[u32] = bytemuck::cast_slice(&data);
            for i in 0..n {
                bits.push(((w[(i / 32) as usize] >> (i % 32)) & 1) as u8);
            }
        }
        staging.unmap();
        done += n;
    }

    let secs = t0.elapsed().as_secs_f64();
    println!(
        "depth {} in {:.2}s  =  {:.0} generations/s",
        depth, secs, depth as f64 / secs
    );

    // --- validation ----------------------------------------------------------
    let k = verify.min(bits.len());
    let reference = cpu_center_column(k);
    let ok = reference == bits[..k];
    println!(
        "GATE: first {} bits vs CPU reference: {}",
        k,
        if ok { "MATCH" } else { "*** MISMATCH ***" }
    );
    if !ok {
        let bad = (0..k).find(|&i| reference[i] != bits[i]).unwrap();
        println!("  first divergence at t={bad}");
        std::process::exit(1);
    }
    let ones = bits.iter().filter(|&&b| b == 1).count();
    println!("ones {} zeros {} ratio {:.9}", ones, bits.len() - ones,
             ones as f64 / (bits.len() - ones) as f64);
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let depth: u32 = a.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let verify: usize = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(20_000);
    pollster::block_on(run(depth, verify));
}
