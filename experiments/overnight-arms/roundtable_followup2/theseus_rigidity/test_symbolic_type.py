from symbolic_type import check, step_rule30, step_rule90


def test_rule30_type_collapses_to_bit():
    pairs = check("Rule30-test", step_rule30, 4000)
    assert set(pairs) <= {(0, 0), (0, 1)}


def test_rule90_type_collapses_to_bit():
    pairs = check("Rule90-test", step_rule90, 4000)
    assert set(pairs) <= {(0, 0), (0, 1)}
