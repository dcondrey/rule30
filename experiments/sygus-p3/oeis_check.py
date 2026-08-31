"""Cross-check the reference simulator against OEIS A051023 (retrieved 2026-08-31
from the raw OEIS data record; offset 0, so a(0) is the seed row)."""
from rule30 import centre_column_naive, centre_column_bitwise

OEIS = [int(x) for x in
"1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,1,0,1,1,1,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1".split(",")]

def main():
    a = centre_column_naive(30, len(OEIS))
    b = centre_column_bitwise(30, len(OEIS))
    assert a == b, "internal simulators disagree"
    assert a == OEIS, f"OEIS mismatch at index {next(i for i,(x,y) in enumerate(zip(a,OEIS)) if x!=y)}"
    print(f"OK: both simulators match all {len(OEIS)} published A051023 terms")

if __name__ == "__main__":
    main()
