"""Pins for the fuel cost model.

Each test here guards a way the instrument could silently break. The
central one is `test_bigint_ops_are_charged_by_width`: if that regresses,
a constant-factor bit-packed candidate reads as an algorithmic
breakthrough, which is the exact false positive this instrument exists to
prevent.
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import fuel  # noqa: E402

CANDIDATES = [
    "sanity_candidates/candidate_a_correct.py",
    "sanity_candidates/candidate_b_wrong.py",
    "sanity_candidates/candidate_c_bitpacked.py",
    "sanity_candidates/candidate_d_lookup_table.py",
    "initial_program.py",
    "reference/simple_reference.py",
]


def run(src, name="f"):
    code = fuel.instrument_source(src)
    m = fuel.FuelMeter()
    g = {fuel.METER_NAME: m}
    m.module_globals = g
    exec(code, g)
    return m, g


def test_bigint_ops_are_charged_by_width():
    """A shift/xor on a W-bit integer must cost ~W/WORD_BITS, never 1."""
    src = "def f(w):\n    x = 1 << w\n    y = x ^ (x >> 1)\n    return y\n"
    m, g = run(src)
    before = m.fuel
    g["f"](100_000)
    cost = m.fuel - before
    expect = 100_000 // fuel.WORD_BITS
    assert cost > expect, f"bigint work charged {cost}, expected > {expect}"
    assert cost < 20 * expect


def test_bigint_charge_scales_linearly_with_width():
    src = "def f(w):\n    x = 1 << w\n    return x ^ (x >> 1)\n"
    m, g = run(src)
    a = m.fuel
    g["f"](100_000)
    c1 = m.fuel - a
    a = m.fuel
    g["f"](200_000)
    c2 = m.fuel - a
    assert 1.8 < c2 / c1 < 2.2, f"doubling width changed cost by {c2 / c1:.3f}x"


def test_sequence_allocation_is_charged_by_length():
    src = "def f(n):\n    return [0] * n\n"
    m, g = run(src)
    before = m.fuel
    g["f"](50_000)
    assert m.fuel - before >= 50_000


def test_loop_iterations_are_charged():
    src = "def f(n):\n    t = 0\n    for i in range(n):\n        pass\n    return t\n"
    m, g = run(src)
    before = m.fuel
    g["f"](10_000)
    assert m.fuel - before >= 10_000


def test_small_int_arithmetic_is_word_cost_not_bit_cost():
    """Loop-index arithmetic must be O(1). Charging it by bit length puts a
    log n factor on the naive simulation and inflates its fitted exponent to
    ~2.15 -- an instrument that cannot recover a known exponent."""
    src = "def f(a, b):\n    return a + b\n"
    m, g = run(src)
    before = m.fuel
    g["f"](40_000, 1)  # a loop index into a width-2n+3 row
    assert m.fuel - before == 1
    # and a value spanning two 30-bit digits costs 2 words, not 41 bits
    before = m.fuel
    g["f"](2**40, 2**40)
    assert m.fuel - before == 2


@pytest.mark.parametrize(
    "src, needle",
    [
        ("import numpy\n", "numpy"),
        ("from os import path\n", "os"),
        ("def f():\n    return eval('1')\n", None),
        ("async def f():\n    pass\n", "AsyncFunctionDef"),
        ("def f(x):\n    yield x\n", "Yield"),
    ],
)
def test_unmodelled_constructs_are_denied(src, needle):
    if needle in ("numpy", "os", "AsyncFunctionDef", "Yield"):
        with pytest.raises(fuel.FuelModelError) as e:
            fuel.instrument_source(src)
        assert needle in str(e.value)
    else:
        # eval() parses fine; it must be denied at CALL time.
        m, g = run(src)
        with pytest.raises(fuel.FuelModelError):
            g["f"]()


@pytest.mark.parametrize("rel", CANDIDATES)
@pytest.mark.parametrize("n", [0, 1, 2, 3, 7, 20, 61, 137, 250])
def test_instrumentation_preserves_semantics(rel, n):
    path = HERE / rel
    plain = fuel.load_plain(path)
    _, got, _setup = fuel.measure_fuel(path, n)
    assert got == plain.center_cell(n)


@pytest.mark.parametrize("rel", CANDIDATES[:3] + [CANDIDATES[4]])
def test_fuel_is_reproducible_in_process(rel):
    path = HERE / rel
    counts = {fuel.measure_fuel(path, 137)[0] for _ in range(3)}
    assert len(counts) == 1


def test_module_level_work_is_reported_as_setup_not_folded_into_the_call():
    """Precomputing at import time must not vanish: a fresh module is exec'd
    per n, so import-time work would otherwise be a free hiding place."""
    _, _, setup = fuel.measure_fuel(HERE / "sanity_candidates/candidate_a_correct.py", 20)
    assert setup == 0
    _, _, cheat = fuel.measure_fuel(HERE / "sanity_candidates/candidate_d_lookup_table.py", 20)
    assert cheat > 4000, "module-level table construction must be counted as setup"


def test_fuel_budget_is_deterministic():
    path = HERE / "sanity_candidates/candidate_a_correct.py"
    with pytest.raises(fuel.FuelExhausted):
        fuel.measure_fuel(path, 500, limit=1000)


def test_chained_comparison_semantics_and_single_evaluation():
    src = (
        "CALLS = []\n"
        "def side(v):\n"
        "    CALLS.append(v)\n"
        "    return v\n"
        "def f(a, b, c):\n"
        "    return a < side(b) < c\n"
    )
    m, g = run(src)
    assert g["f"](1, 2, 3) is True
    assert g["CALLS"] == [2]
    g["CALLS"].clear()
    assert g["f"](5, 2, 3) is False
    assert g["CALLS"] == [2]  # evaluated once, short-circuits after
