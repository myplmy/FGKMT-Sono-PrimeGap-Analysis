import math
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

# ------------------------------------------------------------
# Problem constants
# ------------------------------------------------------------
A = 10**20
B = 10**21
H = 1856
MOD = 2310  # 2*3*5*7*11
DENO = 10**15  # rational certificate denominator

# Exact pi values, independently documented (OEIS A006880 / published tables).
PI_A = 2_220_819_602_560_918_840
PI_B = 21_127_269_486_018_731_928
M_GAPS = PI_B - PI_A - 1  # internal consecutive gaps with both endpoints < B
SPAN = B - A
AVG_GAP = SPAN / M_GAPS

# ------------------------------------------------------------
# Build residue states and the two relevant edge types.
# For a fixed residue transition r -> s, lambda >= 0 means we only
# need the smallest gap of each class:
#   small: 0 < d < H
#   large: d >= H
# Any actual gap with the same residue transition is >= the chosen d,
# so the certificate remains valid.
# ------------------------------------------------------------
def build_edges():
    residues = [r for r in range(MOD) if math.gcd(r, MOD) == 1]
    index = {r: i for i, r in enumerate(residues)}
    edges = []

    for i, r in enumerate(residues):
        for j, s in enumerate(residues):
            diff = (s - r) % MOD
            # Both residues are odd, MOD is even, hence diff is even.
            d0 = diff if diff != 0 else MOD

            # Small representative, if any.
            if d0 < H:
                edges.append((i, j, d0, 0))

            # Smallest representative >= H.
            d1 = d0
            if d1 < H:
                d1 += MOD
            edges.append((i, j, d1, 1))

    return residues, edges

# ------------------------------------------------------------
# Find a floating-point dual certificate.
# Inequality for every allowed transition:
#   w <= lambda*d + mu + phi[i] - phi[j]
# with |phi| <= t.
# Summing over a finite path telescopes the phi terms, giving
#   N_large <= lambda*SPAN + mu*M_GAPS + 2*t.
# ------------------------------------------------------------
def solve_float_certificate(edges, n):
    E = len(edges)
    nv = n + 3  # lambda, mu, phi[n], t

    rows = []
    cols = []
    data = []
    rhs = []

    for k, (i, j, d, w) in enumerate(edges):
        # -lambda*d - mu - phi[i] + phi[j] <= -w
        rows.extend((k, k, k, k))
        cols.extend((0, 1, 2 + i, 2 + j))
        data.extend((-d, -1.0, -1.0, 1.0))
        rhs.append(-w)

    base = E
    for i in range(n):
        k = base + 2*i
        rows.extend((k, k))
        cols.extend((2 + i, nv - 1))
        data.extend((1.0, -1.0))
        rhs.append(0.0)

        k = base + 2*i + 1
        rows.extend((k, k))
        cols.extend((2 + i, nv - 1))
        data.extend((-1.0, -1.0))
        rhs.append(0.0)

    A_ub = coo_matrix((data, (rows, cols)), shape=(E + 2*n, nv)).tocsr()

    c = np.zeros(nv)
    c[0] = AVG_GAP
    c[1] = 1.0
    c[-1] = 2.0 / M_GAPS

    bounds = [(0, None), (None, None)] + [(None, None)] * n + [(0, None)]

    t0 = time.perf_counter()
    res = linprog(
        c,
        A_ub=A_ub,
        b_ub=np.asarray(rhs, dtype=float),
        bounds=bounds,
        method='highs',
    )
    elapsed = time.perf_counter() - t0

    if not res.success:
        raise RuntimeError(res.message)

    return res.x, res.fun, elapsed

# ------------------------------------------------------------
# Convert the floating certificate to a rational certificate and
# verify it with INTEGER arithmetic only.  The LP solver is used only
# to discover a candidate certificate; this phase is the proof check.
# ------------------------------------------------------------
def rationalize_and_verify(x, edges, n):
    D = DENO
    lam_num = round(float(x[0]) * D)
    mu_num = round(float(x[1]) * D)
    phi_num = [int(round(float(v) * D)) for v in x[2:2+n]]
    t_num = max(abs(v) for v in phi_num)

    # Add the smallest possible integer margin to mu until every edge
    # inequality is satisfied exactly.
    margin = 0
    while True:
        mu_try = mu_num + margin
        bad = 0
        min_slack = None
        for i, j, d, w in edges:
            slack = lam_num*d + mu_try + phi_num[i] - phi_num[j] - w*D
            if slack < 0:
                bad += 1
                if min_slack is None or slack < min_slack:
                    min_slack = slack
        if bad == 0:
            mu_num = mu_try
            break
        margin += 1
        if margin > 10_000:
            raise RuntimeError('Could not repair rational certificate')

    # Exact check of |phi_i| <= t.
    assert all(abs(v) <= t_num for v in phi_num)

    # Exact integer verification of every transition inequality.
    min_slack = None
    for i, j, d, w in edges:
        slack = lam_num*d + mu_num + phi_num[i] - phi_num[j] - w*D
        if slack < 0:
            raise AssertionError('Rational certificate failed')
        if min_slack is None or slack < min_slack:
            min_slack = slack

    # Exact rational upper bound for the INTERNAL gaps.
    bound_internal = Fraction(lam_num * SPAN, D) + Fraction(mu_num * M_GAPS, D) + Fraction(2*t_num, D)
    bound_internal_ceiling = (bound_internal.numerator + bound_internal.denominator - 1) // bound_internal.denominator

    # At most one additional large gap can cross the right boundary B.
    # Therefore the target count with starts A <= p < B is <= internal + 1.
    bound_total = bound_internal_ceiling + 1

    return {
        'D': D,
        'lambda_num': lam_num,
        'mu_num': mu_num,
        'phi_num': phi_num,
        't_num': t_num,
        'bound_internal': bound_internal,
        'bound_internal_ceiling': bound_internal_ceiling,
        'bound_total': bound_total,
        'min_slack_scaled': min_slack,
    }


def c_normalization():
    # High precision is deliberately done without relying on float output.
    import mpmath as mp
    mp.mp.dps = 60
    X = mp.mpf(10) ** 21
    L = mp.mpf(9) * 10**20
    h = mp.mpf(1856)
    Q = L / mp.log(X) * mp.e**(-h / mp.log(X))
    return Q


def main():
    print('Preparing 2310-state certificate...')
    print(f'pi(1e20) = {PI_A}')
    print(f'pi(1e21) = {PI_B}')
    print(f'internal gaps = {M_GAPS}')
    print(f'average internal gap upper scale = {AVG_GAP:.15f}')

    residues, edges = build_edges()
    print(f'states = {len(residues)}')
    print(f'edge constraints = {len(edges)}')

    x, float_obj, solve_time = solve_float_certificate(edges, len(residues))
    print(f'LP discovery time = {solve_time:.3f} s')
    print(f'floating optimum fraction = {float_obj:.18g}')

    t0 = time.perf_counter()
    cert = rationalize_and_verify(x, edges, len(residues))
    verify_time = time.perf_counter() - t0

    print(f'exact certificate verification time = {verify_time:.3f} s')
    print(f'minimum scaled slack = {cert["min_slack_scaled"]}')
    print(f'internal-gap upper bound = {cert["bound_internal_ceiling"]}')
    print(f'total target-count upper bound = {cert["bound_total"]}')

    import mpmath as mp
    Q = c_normalization()
    C = mp.mpf(cert['bound_total']) / Q
    print(f'normalized C upper bound = {mp.nstr(C, 30)}')

    # Emit certificate data so an independent verifier can be written
    # without running the LP solver again.
    with open('C2310_certificate.txt', 'w', encoding='utf-8') as f:
        f.write(f'D={cert["D"]}\n')
        f.write(f'lambda_num={cert["lambda_num"]}\n')
        f.write(f'mu_num={cert["mu_num"]}\n')
        f.write(f't_num={cert["t_num"]}\n')
        f.write('phi_num=' + ','.join(map(str, cert['phi_num'])) + '\n')
        f.write(f'internal_bound={cert["bound_internal_ceiling"]}\n')
        f.write(f'total_bound={cert["bound_total"]}\n')

    print('Wrote C2310_certificate.txt')


if __name__ == '__main__':
    main()
