"""Verify, exactly: (a) the two pin/pass identities; (b) that the LHP x<=-1 is a
function of the centre column c and the LHP's own t=0 data alone (no r needed);
(c) that the driven_lhp helper reproduces the true lone-seed LHP."""
import sys
sys.path.insert(0, 'uc/r1-r1zero')
from r1zero_lib import driven_lhp

T = 400
OFF = T + 4
row = 1 << OFF                      # lone seed at x=0
S = []                              # S[t] = full row int
for _ in range(T + 2):
    S.append(row)
    row = (row << 1) ^ (row | (row >> 1))

def cell(t, x):
    return (S[t] >> (OFF + x)) & 1

c = [cell(t, 0) for t in range(T + 2)]
r = [cell(t, 1) for t in range(T + 2)]
l = [cell(t, -1) for t in range(T + 2)]

pin_tests = pin_fail = pass_tests = pass_fail = 0
for t in range(T):
    if c[t] == 1:
        pin_tests += 1
        pin_fail += (l[t] != (1 ^ c[t + 1]))
    else:
        pass_tests += 1
        pass_fail += (l[t] != (c[t + 1] ^ r[t]))
print(f"(a) pin  c_t=1 -> l_t = NOT c_(t+1):     {pin_tests} tests, {pin_fail} failures")
print(f"(a) pass c_t=0 -> l_t = c_(t+1) XOR r_t: {pass_tests} tests, {pass_fail} failures")

# (b)/(c) driven_lhp from c alone, zero LHP initial data
rows = driven_lhp(c, T)
mism = [t for t in range(T + 1) for i in range(1, T + 1) if ((rows[t] >> i) & 1) != cell(t, -i)]
print(f"(b) LHP from c alone vs true LHP over t<=%d, x in [-%d,-1]: %d mismatches" % (T, T, len(mism)))
