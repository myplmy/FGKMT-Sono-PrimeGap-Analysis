import math
from fractions import Fraction

A = 10**20
B = 10**21
H = 1856
MOD = 2310
DENO = 10**15
PI_A = 2_220_819_602_560_918_840
PI_B = 21_127_269_486_018_731_928
M_GAPS = PI_B - PI_A - 1
SPAN = B - A


def build_edges():
    residues = [r for r in range(MOD) if math.gcd(r, MOD) == 1]
    edges = []
    for i, r in enumerate(residues):
        for j, s in enumerate(residues):
            diff = (s - r) % MOD
            d0 = diff if diff != 0 else MOD
            if d0 < H:
                edges.append((i, j, d0, 0))
            d1 = d0 if d0 >= H else d0 + MOD
            edges.append((i, j, d1, 1))
    return residues, edges


def read_certificate(path='C2310_certificate.txt'):
    d = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            k, v = line.rstrip('\n').split('=', 1)
            if k == 'phi_num':
                d[k] = [int(x) for x in v.split(',')]
            elif k in {'D','lambda_num','mu_num','t_num','internal_bound','total_bound'}:
                d[k] = int(v)
            else:
                d[k] = v
    return d


def verify(cert):
    D = cert['D']
    lam = cert['lambda_num']
    mu = cert['mu_num']
    phi = cert['phi_num']
    t = cert['t_num']
    assert D == DENO
    assert len(phi) == 480
    assert max(abs(v) for v in phi) <= t

    residues, edges = build_edges()
    min_slack = None
    for i, j, gap, weight in edges:
        lhs = lam * gap + mu + phi[i] - phi[j]
        rhs = weight * D
        slack = lhs - rhs
        if slack < 0:
            raise AssertionError(f'certificate failure on edge {i}->{j}, gap={gap}, weight={weight}, slack={slack}')
        min_slack = slack if min_slack is None else min(min_slack, slack)

    bound = Fraction(lam * SPAN, D) + Fraction(mu * M_GAPS, D) + Fraction(2*t, D)
    bound_ceiling = (bound.numerator + bound.denominator - 1) // bound.denominator
    total_bound = bound_ceiling + 1
    assert bound_ceiling == cert['internal_bound']
    assert total_bound == cert['total_bound']

    print('PASS')
    print('states:', len(residues))
    print('edge constraints:', len(edges))
    print('minimum integer slack:', min_slack)
    print('internal large-gap bound:', bound_ceiling)
    print('total large-gap bound (including at most one boundary-crossing gap):', total_bound)


if __name__ == '__main__':
    verify(read_certificate())
