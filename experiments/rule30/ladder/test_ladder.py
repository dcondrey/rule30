"""Regression and calibration tests for the periodicity ladder (route R7).

Every test pins either a soundness fact (constraints hold on the true
lone-seed diagram) or a known-answer calibration (theorems this repo already
holds on paper must be rederived mechanically; Rule 90's true behavior must
stay admissible).
"""

from ladder import Params, decide, regression, verify_witness


def test_transduction_matches_simulation_rule30():
    for R, k in ((1, 1), (2, 2), (3, 2), (4, 1)):
        mismatches, ok = regression(30, R, k, T=300)
        assert mismatches == 0, (R, k, mismatches)
        assert ok, (R, k)


def test_transduction_matches_simulation_rule90():
    for R, k in ((1, 1), (2, 2), (3, 2)):
        mismatches, ok = regression(90, R, k, T=300)
        assert mismatches == 0, (R, k, mismatches)
        assert ok, (R, k)


def test_calibration_A1_constant_one_empties():
    # Pin: c(t)=1 forever forces col_{-1}=0 forever; Diff_1 must be empty.
    P = Params(rule=30, right_depth=1, left_depth=1,
               period_word=(1,), diff_q=1)
    res = decide(P)
    assert res["verdict"] == "EMPTY", res


def test_calibration_A2_zero_tail_open_at_R1():
    # Without right-extension constraints col_{-1}=r is free: nonempty.
    P = Params(rule=30, right_depth=1, left_depth=1,
               period_word=(0,), diff_q=1)
    res = decide(P)
    assert res["verdict"] == "NONEMPTY", res
    okv, note = verify_witness(res["witness"]["prefix"],
                               res["witness"]["cycle"], P)
    assert okv, note


def test_calibration_A3_zero_tail_empties_at_R2():
    # The pin at column 1 makes r eventually constant under c=0 tail;
    # mechanical rederivation of the zero-tail corollary.
    P = Params(rule=30, right_depth=2, left_depth=1,
               period_word=(0,), diff_q=1)
    res = decide(P)
    assert res["verdict"] == "EMPTY", res


def test_calibration_B_rule90_stays_nonempty():
    # Rule 90's lone-seed center IS eventually zero: the pipeline must not
    # exclude it at any depth we can afford.  Emptiness = soundness bug.
    for R in (1, 2, 3, 4):
        P = Params(rule=90, right_depth=R, left_depth=1,
                   period_word=(0,), diff_q=1)
        res = decide(P)
        assert res["verdict"] == "NONEMPTY", (R, res)
        okv, note = verify_witness(res["witness"]["prefix"],
                                   res["witness"]["cycle"], P)
        assert okv, (R, note)


def test_tail_word_rotation_equivalence():
    # "01" and "10" define the same eventually-periodic language when the
    # onset is existentially quantified; verdicts must agree.
    for R in (1, 2, 3):
        a = decide(Params(rule=30, right_depth=R, left_depth=1,
                          period_word=(0, 1), diff_q=2))
        b = decide(Params(rule=30, right_depth=R, left_depth=1,
                          period_word=(1, 0), diff_q=2))
        assert a["verdict"] == b["verdict"], (R, a, b)
