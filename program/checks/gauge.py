"""Gauge results on the cyclic world: K66, K67, K68, K70, K71 and the simulation half of K72.

Task S-02, foundations.md section 7 checks 1 to 4. Pre-registration for the simulations, hand
proofs and findings: gauge.md. All checks are witness checks: exact `Fraction` arithmetic on
finite worlds, exhaustive over the stated groups. Each statement below names its search space.
`no-counterexample` on a finite instance is evidence for the universal claim, never proof of it.

Data shapes. A world is (P, K): P[w] is a law on Omega = {0..N-1} and K[w][a] a kernel into
words a. Speaking emits a two-word string (a, b), the two words independent given w, so the
corpus law is D[(a, b)] = sum_w P[w] K[w][a] K[w][b]. A bijection g is a tuple with g[w] the
image of w. The gauge action is g.(P, K) = (g P, K o g^-1): P'[g[w]] = P[w], K'[g[w]] = K[w].
A sensorium is a tuple sigma[w] of observation labels. Its joint law with the words is
J[(o, a, b)].

Cyclic worlds: Omega = Z_N, P uniform (the stationary law of t mod N in cyclic_world.py) unless
a check says otherwise, and K[w][a] proportional to kappa[(a - w) mod N], with kappa the
cyclic-world seasonal profile rounded to integers.

Witness conventions (witness.verdict): a counterexample needs every hypothesis true and a gap
above 1e-9. Any precondition that must hold raises instead of returning False, so a broken
encoding reads as `error`, never as a vacuous pass.
"""
import hashlib
import itertools
import math
import random
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from check import Check

_CW = Path(__file__).resolve().parents[1] / "experiments" / "cyclic_world"
sys.path.insert(0, str(_CW))
import cyclic_world as cw  # noqa: E402
import naming_game as ng  # noqa: E402

# The simulator and the testbed are pinned: changing either turns the verdicts into errors until
# the pin is updated, which also makes this module (and so every verdict) stale. gauge.md Part A.
PINS = {"naming_game.py": "d4237674fe32826318cd1c028f1e2ac37db6979059cc9e59a4b39f5b05360256",
        "cyclic_world.py": "8886c87e26d467b77d76ae1e83f525fd98bbcac6a1b3feee8ce1581bdddbed06"}


def pin(name):
    got = hashlib.sha256((_CW / name).read_bytes()).hexdigest()
    if got != PINS[name]:
        raise RuntimeError(f"{name} changed after pre-registration (sha256 {got[:12]}, pinned {PINS[name][:12]})")


# Groups and worlds -----------------------------------------------------------------------------

def rotations(N):
    return [tuple((w + s) % N for w in range(N)) for s in range(N)]


def reflections(N):
    return [tuple((s - w) % N for w in range(N)) for s in range(N)]


def dihedral(N):
    """D_N acting on Z_N. Faithful for N >= 3, so it has 2N elements."""
    if N < 3:
        raise ValueError("D_N is faithful on Z_N only for N >= 3")
    return rotations(N) + reflections(N)


def sym(N):
    return list(itertools.permutations(range(N)))


def kappa(N, profile=None):
    pin("cyclic_world.py")
    prof = cw.default_profile(N) if profile is None else profile
    return [max(1, round(100 * float(x))) for x in prof]


def cyc_world(N, kap, P=None):
    tot = sum(kap)
    K = tuple(tuple(Fraction(kap[(a - w) % N], tot) for a in range(N)) for w in range(N))
    P = tuple(Fraction(1, N) for _ in range(N)) if P is None else tuple(P)
    return P, K


def rand_law(n, seed):
    rng = random.Random(seed)
    v = [rng.randint(1, 9) for _ in range(n)]
    return tuple(Fraction(x, sum(v)) for x in v)


def rand_world(N, seed):
    """Generic rational P and generic row-stochastic K, no symmetry at all."""
    return rand_law(N, seed), tuple(rand_law(N, seed * 1000 + w + 1) for w in range(N))


def act(g, P, K):
    P2, K2 = [None] * len(P), [None] * len(P)
    for w in range(len(P)):
        P2[g[w]] = P[w]
        K2[g[w]] = K[w]
    return tuple(P2), tuple(K2)


def corpus(P, K):
    n = len(P)
    return {(a, b): sum(P[w] * K[w][a] * K[w][b] for w in range(n)) for a in range(len(K[0])) for b in range(len(K[0]))}


def joint(P, K, sigma):
    out = {}
    for w in range(len(P)):
        for a in range(len(K[w])):
            for b in range(len(K[w])):
                key = (sigma[w], a, b)
                out[key] = out.get(key, 0) + P[w] * K[w][a] * K[w][b]
    return out


def anchor(N, a):
    return tuple(int(w == a) for w in range(N))


def quant(N, q):
    return tuple(w // q for w in range(N))


def stabilizer(group, sigma):
    return [g for g in group if all(sigma[g[w]] == sigma[w] for w in range(len(sigma)))]


def surviving(group, P, K, sigma):
    """{g in group : the joint law of (sigma, words) is the same under g.(P, K)}"""
    base = joint(P, K, sigma)
    return [g for g in group if joint(*act(g, P, K), sigma) == base]


def tv(K1, K2):
    return max(float(sum(abs(x - y) for x, y in zip(r1, r2)) / 2) for r1, r2 in zip(K1, K2))


def expect_count(got, want, what):
    if got != want:
        raise RuntimeError(f"{what}: searched {got} instances, expected {want}")


# K66 -------------------------------------------------------------------------------------------

def k66_orbit_invariance():
    """D unchanged by every g, exact. Sym(5) on a generic world, D_12 on the default cyclic world."""
    worst, n = Fraction(0), 0
    for (P, K), group in ((rand_world(5, 1), sym(5)), (cyc_world(12, kappa(12)), dihedral(12))):
        D = corpus(P, K)
        for g in group:
            D2 = corpus(*act(g, P, K))
            worst = max(worst, max(abs(D2[k] - D[k]) for k in D))
            n += 1
    expect_count(n, 120 + 24, "K66 orbit invariance")
    return {"every g in Sym(5) on a generic world, every g in D_12 on the cyclic world": True}, float(worst)


def k66_reference_identifiable():
    """Witness: the corpus law does not determine the pair. All 11 nontrivial shifts of Z_12 give a different
    world with the same D. gap = the least separation (total variation of the speaking kernels)."""
    P, K = cyc_world(12, kappa(12))
    D = corpus(P, K)
    gaps, same = [], True
    for s in range(1, 12):
        g = rotations(12)[s]
        P2, K2 = act(g, P, K)
        same &= corpus(P2, K2) == D
        gaps.append(tv(K, K2))
    return {"corpus laws are equal, exactly, for every shift": same,
            "the shifted worlds differ from the original": min(gaps) > 0}, min(gaps)


def k66_geometry():
    """The geometry D induces on the vocabulary is a circle fixed up to D_N. Aut(D) = {tau in Sym(V): D(tau a, tau b)
    = D(a, b)} equals D_N exactly for N = 6 and N = 7 (all 720 and 5040 permutations), and contains D_12."""
    n = 0
    for N in (6, 7):
        P, K = cyc_world(N, kappa(N))
        D = corpus(P, K)
        aut = {t for t in sym(N) if all(D[(t[a], t[b])] == D[(a, b)] for a in range(N) for b in range(N))}
        n += math.factorial(N)
        if aut != set(dihedral(N)):
            return {"the search found a violation": True}, max(1.0, float(len(aut) - 2 * N))
    P, K = cyc_world(12, kappa(12))
    D = corpus(P, K)
    ok = all(D[(t[a], t[b])] == D[(a, b)] for t in dihedral(12) for a in range(12) for b in range(12))
    expect_count(n, 720 + 5040, "K66 geometry")
    return {"Aut(D) = D_N for N = 6, 7, and D_12 acts by isometries": True}, 0.0 if ok else 1.0


def half_action_changes_corpus():
    """Sanity: moving only the speaker (not P) is not a gauge move. A generic world loses D under it."""
    P, K = rand_world(5, 2)
    D = corpus(P, K)
    g = (1, 2, 0, 4, 3)
    _, K2 = act(g, P, K)
    D2 = corpus(P, K2)
    return {"g is a nontrivial bijection": g != tuple(range(5))}, float(max(abs(D2[k] - D[k]) for k in D))


# K67 -------------------------------------------------------------------------------------------

def k67_containment():
    """Every g with sigma o g = sigma preserves J. Sym(6) on the default cyclic world with five sensoria, Sym(5) on a
    generic world with three. Stabilizer sizes are asserted, so a vacuous loop reads as an error."""
    worst, sizes = Fraction(0), []
    cases = [(cyc_world(6, kappa(6)), sym(6), [anchor(6, 0), quant(6, 2), quant(6, 3), tuple(range(6)), (0,) * 6]),
             (rand_world(5, 3), sym(5), [anchor(5, 1), quant(5, 2), (0,) * 5])]
    for (P, K), group, sigmas in cases:
        for sigma in sigmas:
            base = joint(P, K, sigma)
            stab = stabilizer(group, sigma)
            sizes.append(len(stab))
            for g in stab:
                J = joint(*act(g, P, K), sigma)
                worst = max(worst, max(abs(J[k] - base[k]) for k in base))
    expect_count(sizes, [120, 8, 36, 1, 720, 24, 4, 120], "K67 stabilizer sizes")
    return {"every g in Stab(sigma) in every case": True}, float(worst)


def surviving_gauge_ratio(P, K, group, sigmas):
    """For each sigma, |S(sigma)| - |Stab(sigma)| where S is the surviving gauge; 0 means equality."""
    out = []
    for sigma in sigmas:
        S, st = surviving(group, P, K, sigma), stabilizer(group, sigma)
        if not set(st) <= set(S):
            raise RuntimeError("containment failed inside the equality test")
        out.append(len(S) - len(st))
    return out


def k67_equality_generic():
    """On the default cyclic world at N = 6 the surviving gauge in Sym(6) equals the stabilizer, for each sensorium."""
    P, K = cyc_world(6, kappa(6))
    extra = surviving_gauge_ratio(P, K, sym(6), [anchor(6, 0), quant(6, 2), quant(6, 3), tuple(range(6))])
    return {"S = Stab for all four sensoria": True}, float(sum(extra))


def hemisphere_blind_world():
    """N = 12 world whose speaking profile has period N/2: corpus_profile(World(12), 1/2), the S4 case. Words carry no
    hemisphere. Shift by 6 maps the pair to itself, so it survives every sensorium."""
    prof = cw.corpus_profile(cw.World(12), 0.5)
    kap = kappa(12, prof)
    if any(kap[d] != kap[(d + 6) % 12] for d in range(12)):
        raise RuntimeError("profile is not N/2-periodic")
    return cyc_world(12, kap)


def k67_equality_witness(sigma_name):
    def run():
        P, K = hemisphere_blind_world()
        sigma = tuple(range(12)) if sigma_name == "identity" else anchor(12, 0)
        g = rotations(12)[6]
        moved = sum(sigma[g[w]] != sigma[w] for w in range(12)) / 12
        same = joint(*act(g, P, K), sigma) == joint(P, K, sigma)
        return {"sigma o g != sigma": moved > 0, "the joint law of (sigma, words) is the same": same}, moved
    return run


def k67_no_gauge_is_free():
    """Sanity: the joint law is not invariant under every bijection. Some g outside Stab(sigma) moves it on a generic world."""
    P, K = rand_world(5, 4)
    sigma = anchor(5, 0)
    base = joint(P, K, sigma)
    g = (1, 0, 2, 3, 4)
    J = joint(*act(g, P, K), sigma)
    return {"sigma o g != sigma": stabilizer([g], sigma) == []}, float(max(abs(J[k] - base[k]) for k in base))


# K68 -------------------------------------------------------------------------------------------

def pointwise(group, A):
    return [h for h in group if all(h[a] == a for a in A)]


def k68_free_action():
    """Z_N acts freely, so H_A is trivial for every nonempty anchor set A: all A for N = 3..12, all singletons to 16."""
    n = 0
    for N in range(3, 17):
        subsets = (itertools.chain.from_iterable(itertools.combinations(range(N), k) for k in range(1, N + 1))
                   if N <= 12 else [(a,) for a in range(N)])
        for A in subsets:
            if len(pointwise(rotations(N), A)) != 1:
                return {"the search found a violation": True}, 1.0
            n += 1
    expect_count(n, sum(2 ** N - 1 for N in range(3, 13)) + sum(range(13, 17)), "K68 free action")
    return {"H_A is {id} under Z_N for every nonempty A searched": True}, 0.0


def k68_dihedral_one_anchor():
    """Under D_N one anchor leaves exactly one reflection, the one through the anchor, for N = 3..16, odd and even."""
    n = 0
    for N in range(3, 17):
        for a in range(N):
            H = pointwise(dihedral(N), (a,))
            want = {tuple(range(N)), tuple((2 * a - w) % N for w in range(N))}
            if set(H) != want or len(H) != 2:
                return {"the search found a violation": True}, 1.0
            n += 1
    expect_count(n, sum(range(3, 17)), "K68 dihedral")
    return {"H_{a} has order 2 for every N and anchor searched": True}, 0.0


def k68_freeness_load_bearing():
    """Probe: drop freeness. D_N is not free, and for one anchor H_A is not trivial. gap = |H_A| - 1."""
    sizes = [len(pointwise(dihedral(N), (0,))) for N in range(3, 17)]
    nonfree = all(any(h != tuple(range(N)) and any(h[w] == w for w in range(N)) for h in dihedral(N)) for N in range(3, 17))
    return {"A is nonempty": True, "D_N has a nonidentity element with a fixed point": nonfree}, float(min(sizes) - 1)


def k68_surviving_gauge():
    """Cyclic-world version. With one anchor sensorium on the default world at N = 12, the surviving gauge inside D_12 is
    exactly {id, reflection through the anchor}, for every anchor. No nontrivial rotation survives."""
    P, K = cyc_world(12, kappa(12))
    n = 0
    for a in range(12):
        S = surviving(dihedral(12), P, K, anchor(12, a))
        if set(S) != {tuple(range(12)), tuple((2 * a - w) % 12 for w in range(12))}:
            return {"the search found a violation": True}, 1.0
        n += 1
    expect_count(n, 12, "K68 surviving gauge")
    return {"S(anchor a) within D_12 is {id, r_a} for all 12 anchors": True}, 0.0


def k68_two_anchors():
    """Probe, beyond the charter. Two anchors in D_N leave a reflection exactly when they are antipodal (N even)."""
    for N in range(4, 17):
        for a, b in itertools.combinations(range(N), 2):
            size = len(pointwise(dihedral(N), (a, b)))
            antipodal = N % 2 == 0 and (b - a) % N == N // 2
            if size != (2 if antipodal else 1):
                return {"the search found a violation": True}, 1.0
    return {"|H_A| = 2 iff the anchors are antipodal, for N = 4..16": True}, 0.0


# K70 -------------------------------------------------------------------------------------------

def mutual_information(P, X):
    """I(Omega; Y) in bits from exact P and kernel rows X."""
    n, m = len(P), len(X[0])
    q = [sum(P[w] * X[w][y] for w in range(n)) for y in range(m)]
    return sum(float(P[w] * X[w][y]) * math.log2(float(X[w][y] / q[y]))
               for w in range(n) for y in range(m) if P[w] * X[w][y] > 0)


def k70_exact():
    """The joint law of (Omega, Y) is relabeled exactly by g, so I is unchanged: Sym(5) and D_12, generic P and X."""
    worst, n = 0.0, 0
    for N, group, seed in ((5, sym(5), 5), (12, dihedral(12), 6)):
        P, X = rand_world(N, seed)
        base = mutual_information(P, X)
        for g in group:
            P2, X2 = act(g, P, X)
            if any(P2[g[w]] * X2[g[w]][y] != P[w] * X[w][y] for w in range(N) for y in range(N)):
                raise RuntimeError("joint law is not the relabeled joint law")
            worst = max(worst, abs(mutual_information(P2, X2) - base))
            n += 1
    expect_count(n, 120 + 24, "K70 exact")
    return {"every g in Sym(5) and D_12 relabels the joint law exactly": True}, worst


def k70_testbed():
    """grounded_information from the cyclic world, in floating point: every g in D_12 and Sym(5), for the uniform and the
    seasonal prior, with random, box-blur and noiseless kernels."""
    import numpy as np
    pin("cyclic_world.py")
    rng = np.random.default_rng(11)
    worst, n = 0.0, 0
    for N, group in ((12, dihedral(12)), (5, sym(5))):
        priors = [np.full(N, 1.0 / N), cw.default_profile(N) / cw.default_profile(N).sum()]
        rk = rng.random((N, N))
        kernels = [rk / rk.sum(1, keepdims=True), cw.Channel.box_blur(N, 3).K, cw.Channel.noiseless(N).K]
        for prior in priors:
            for K in kernels:
                base = cw.grounded_information(prior, K)
                for g in group:
                    perm = np.array(g)
                    p2, K2 = np.empty(N), np.empty_like(K)
                    p2[perm], K2[perm] = prior, K
                    worst = max(worst, abs(cw.grounded_information(p2, K2) - base))
                    n += 1
    expect_count(n, 2 * 3 * (24 + 120), "K70 testbed")
    return {"grounded_information(g P, K o g^-1) = grounded_information(P, K)": True}, worst


def half_action_changes_information():
    """Sanity: moving only the prior is not a gauge move; I changes on a generic world."""
    P, X = rand_world(5, 7)
    g = (1, 2, 0, 4, 3)
    P2, _ = act(g, P, X)
    return {"g is a nontrivial bijection": g != tuple(range(5))}, abs(mutual_information(P2, X) - mutual_information(P, X))


# K71, K72.c: exact small population --------------------------------------------------------------

M3, m3 = 3, 3
S3 = list(itertools.permutations(range(m3)))
EMPTY = (0,) * M3


@lru_cache(maxsize=None)
def chain(r):
    pin("naming_game.py")
    T = ng.kernel(M3, m3, [r, 1, 1])
    return T, ng.absorption(T, M3, m3)


def equivariance_gap(T, perms):
    """Largest |T(pi s -> pi s') - T(s -> s')| over every state, successor and pi, exact."""
    worst = Fraction(0)
    for s, row in T.items():
        for p in perms:
            moved = {ng.relabel(s2, p): q for s2, q in row.items()}
            other = T[ng.relabel(s, p)]
            for k in set(moved) | set(other):
                worst = max(worst, abs(moved.get(k, 0) - other.get(k, 0)))
    return worst


def k71_equivariant_attractors():
    T, _ = chain(1)
    absorbing = sorted(s for s, row in T.items() if row == {s: 1})
    cons = sorted(ng.consensus_states(M3, m3))
    closed = all(ng.relabel(s, p) in cons for s in cons for p in S3)
    orbit = {ng.relabel(cons[0], p) for p in S3}
    gap = float(equivariance_gap(T, S3))
    if not (len(T) == 120 and absorbing == cons and closed and orbit == set(cons)):
        gap = max(gap, 1.0)  # the absorbing states are not the 3 consensus states, or they are not one S-orbit
    return {"every state, successor and permutation searched": True}, gap


def k71_invariant_law():
    """The law at each step t = 0..8 from the empty state is S-invariant: exact."""
    T, _ = chain(1)
    law, worst = {EMPTY: Fraction(1)}, Fraction(0)
    for t in range(9):
        for s, p in law.items():
            for pi in S3:
                worst = max(worst, abs(law.get(ng.relabel(s, pi), 0) - p))
        law = ng.step_law(law, T)
    if not all(ng.relabel(EMPTY, p) == EMPTY for p in S3):
        raise RuntimeError("the initial state is not S-fixed")
    return {"every step t = 0..8 searched": True}, float(worst)


def k71_symmetric_states_transient():
    """No recurrent class except the consensus states, so absorption is certain; the S-fixed states are transient and
    reach each consensus with probability exactly 1/3. The chain is lumped over anonymous agents, so a multiset is
    S-fixed when relabeling permutes its inventories among themselves: the empty and full inventories, and also
    mixtures such as one agent per single form. All of them are searched."""
    T, h = chain(1)
    fixed = sorted(s for s in T if all(ng.relabel(s, p) == s for p in S3))
    if not {(0, 0, 0), (7, 7, 7)} <= set(fixed):
        raise RuntimeError("the empty and full states must be S-fixed")
    third = [Fraction(1, 3)] * 3
    ok = all(sum(v) == 1 for v in h.values()) and all(T[s] != {s: 1} and h[s] == third for s in fixed)
    return {"all 120 states and every S-fixed multiset searched": True}, 0.0 if ok else 1.0


def k71_broken_kernel_detected():
    """Sanity: the same equivariance test over the full S on the r = 2 kernel finds a violation."""
    T, _ = chain(2)
    return {"the kernel has cheap form 0": True}, float(equivariance_gap(T, S3))


def k72_exact_direction(r):
    def run():
        _, h = chain(r)
        h0 = h[EMPTY][0]
        floor = Fraction(1, 3) + Fraction(1, 100) * (r - 1)
        return {"r is the weight of the cheap form": True}, float(floor - h0) if sum(h[EMPTY]) == 1 else 1.0
    return run


def k72_exact_residual():
    _, h = chain(2)
    _, h3 = chain(3)
    gap = max(abs(h[EMPTY][1] - h[EMPTY][2]), abs(h3[EMPTY][1] - h3[EMPTY][2]))
    return {"r = 2 and r = 3": True}, float(gap)


def k72_exact_monotone():
    p = [chain(r)[1][EMPTY][0] for r in (1, 2, 3)]
    return {"r = 1, 2, 3": True}, float(max(p[0] - p[1], p[1] - p[2]))


# K71, K72.c: ensemble over seeds (pre-registered in gauge.md Part A) ----------------------------

M_POP, M_FORMS, T_MAX, R_SEEDS = 20, 5, 50_000, 2000
TAU, TAU_RESIDUAL, MIN_CONVERGED = 0.036, 0.040, 0.99


@lru_cache(maxsize=None)
def ens(config):
    pin("naming_game.py")
    r = (1.0, 2.0, 3.0)[config]
    return ng.ensemble(M_POP, M_FORMS, r, R_SEEDS, T_MAX, config)


def shares(config):
    e = ens(config)
    return [c / e["converged"] for c in e["counts"]]


def sim_converged():
    return {"all three configurations run": True}, MIN_CONVERGED - min(ens(c)["converged"] / R_SEEDS for c in range(3))


def sim_control_symmetric():
    p = shares(0)
    return {"r = 1": True}, max(abs(x - 1 / M_FORMS) for x in p) - TAU


def sim_cheaper_favored(config):
    def run():
        return {f"r = {(1, 2, 3)[config]}": True}, (1 / M_FORMS + TAU) - shares(config)[0]
    return run


def sim_monotone():
    return {"r = 2 to r = 3": True}, -TAU - (shares(2)[0] - shares(1)[0])


def sim_residual():
    worst = 0.0
    for c in (1, 2):
        p = shares(c)
        rest = (1 - p[0]) / (M_FORMS - 1)
        worst = max(worst, max(abs(x - rest) for x in p[1:]))
    return {"r = 2 and r = 3": True}, worst - TAU_RESIDUAL


CHECKS = [
    Check("gauge/sanity-half-action-corpus", None, "sanity", "witness", "counterexample",
          "Moving only the speaker, not P, changes the corpus law on a generic world: the K66 test can see a non-gauge move",
          half_action_changes_corpus),
    Check("gauge/sanity-half-action-info", None, "sanity", "witness", "counterexample",
          "Moving only the prior changes I(Omega; Y) on a generic world: the K70 test can see a non-gauge move",
          half_action_changes_information),
    Check("gauge/sanity-outside-stabilizer", None, "sanity", "witness", "counterexample",
          "A bijection outside Stab(sigma) changes the joint law of (sigma, words) on a generic world: the K67 test can see it",
          k67_no_gauge_is_free),
    Check("gauge/sanity-broken-kernel", None, "sanity", "witness", "counterexample",
          "The r = 2 naming-game kernel fails S-equivariance over the full Sym(F): the K71 test can see broken symmetry",
          k71_broken_kernel_detected),

    Check("K66.cyclic-world/orbit-invariance", "K66.cyclic-world", "proves", "witness", "no-counterexample",
          "Exact: D(g.(P, K)) = D(P, K) for all 120 g in Sym(5) on a generic world and all 24 g in D_12 on the default cyclic world",
          k66_orbit_invariance),
    Check("K66.geometry/circle-up-to-D_N", "K66.geometry", "proves", "witness", "no-counterexample",
          "Exact: the geometry D induces on the vocabulary has automorphism group exactly D_N for N = 6 (720 perms) and N = 7 (5040), and D_12 acts by isometries",
          k66_geometry),
    Check("K66~reference-identifiable/shift-witness", "K66~reference-identifiable", "refutes", "witness", "counterexample",
          "Z_12: all 11 nontrivial shifts give a different world (speaking kernels at positive total variation) with exactly the same corpus law, so D does not determine reference",
          k66_reference_identifiable),

    Check("K67.containment/exhaustive", "K67.containment", "proves", "witness", "no-counterexample",
          "Exact: every g with sigma o g = sigma leaves the joint law of (sigma, words) unchanged; 8 (world, sensorium) cases, Sym(6) and Sym(5), 120 + 8 + 36 + 1 + 720 + 24 + 4 + 120 stabilizer elements",
          k67_containment),
    Check("K67.equality-generic/Sym6", "K67.equality-generic", "probe", "witness", "no-counterexample",
          "Exact: on the default cyclic world at N = 6 the surviving gauge in Sym(6) equals Stab(sigma) for four sensoria",
          k67_equality_generic),
    Check("K67~equality/hemisphere-identity", "K67~equality", "refutes", "witness", "counterexample",
          "N = 12, speaking profile of period 6, sigma = identity: the shift by 6 is outside Stab(sigma) yet leaves the joint law unchanged, so the surviving gauge is strictly larger than the stabilizer",
          k67_equality_witness("identity")),
    Check("K67~equality/hemisphere-anchor", "K67~equality", "refutes", "witness", "counterexample",
          "N = 12, speaking profile of period 6, one anchor at 0: the shift by 6 is outside Stab(sigma) yet leaves the joint law unchanged, so one anchor does not fix the rotation here",
          k67_equality_witness("anchor")),

    Check("K68.cyclic-world/free-action", "K68.cyclic-world", "proves", "witness", "no-counterexample",
          "Exact: H_A is trivial in Z_N for every nonempty A, all subsets for N = 3..12 and all singletons for N = 13..16",
          k68_free_action),
    Check("K68.cyclic-world/dihedral-one-anchor", "K68.cyclic-world", "proves", "witness", "no-counterexample",
          "Exact: in D_N with one anchor a, H_A = {id, w -> 2a - w} has order 2, for every N = 3..16 (odd and even) and every a",
          k68_dihedral_one_anchor),
    Check("K68.cyclic-world/surviving-gauge", "K68.cyclic-world", "proves", "witness", "no-counterexample",
          "Exact: on the default cyclic world at N = 12 with a one-anchor sensorium, the surviving gauge inside D_12 is {id, r_a} for each of the 12 anchors",
          k68_surviving_gauge),
    Check("K68/freeness-load-bearing", "K68", "probe", "witness", "counterexample",
          "Drop freeness: D_N acts non-freely and one anchor leaves |H_A| = 2, so 'H_A trivial' fails for N = 3..16",
          k68_freeness_load_bearing),
    Check("K68/two-anchors", "K68", "probe", "witness", "no-counterexample",
          "Exact, N = 4..16, all anchor pairs: |H_A| in D_N is 2 when the anchors are antipodal (N even) and 1 otherwise",
          k68_two_anchors),

    Check("K70.cyclic-world/exact-joint", "K70.cyclic-world", "proves", "witness", "no-counterexample",
          "Exact joint law of (Omega, Y) is relabeled by g, and I is unchanged, for all 120 g in Sym(5) and all 24 g in D_12 (rotations and reflections) on generic worlds",
          k70_exact),
    Check("K70.cyclic-world/testbed-numeric", "K70.cyclic-world", "probe", "witness", "no-counterexample",
          "cyclic_world.grounded_information is unchanged to 1e-9 under every g in D_12 and Sym(5): 2 priors x 3 kernels (random, box blur, noiseless) x 144 g",
          k70_testbed),

    Check("K71.small-population/attractors-equivariance", "K71.small-population", "proves", "witness", "no-counterexample",
          "Exact, 3 agents and 3 forms, all 120 multiset states and all 6 permutations: the kernel is S-equivariant, and the absorbing states are the 3 consensus states, one S-orbit (K71 a)",
          k71_equivariant_attractors),
    Check("K71.small-population/invariant-law", "K71.small-population", "proves", "witness", "no-counterexample",
          "Exact: from the empty state the law at each step t = 0..8 is S-invariant (K71 b)",
          k71_invariant_law),
    Check("K71.small-population/symmetric-transient", "K71.small-population", "proves", "witness", "no-counterexample",
          "Exact: absorption into a consensus has probability 1 from every state, the S-fixed states (every S-fixed multiset, including empty and full) are transient, each consensus has probability 1/3 from them (K71 c, finite form)",
          k71_symmetric_states_transient),
    Check("K72.c/exact-direction-r2", "K72.c", "proves", "witness", "no-counterexample",
          "Exact, 3 agents and 3 forms, w = (2,1,1): P(consensus 0 from empty) >= 1/3 + 1/100",
          k72_exact_direction(2)),
    Check("K72.c/exact-direction-r3", "K72.c", "proves", "witness", "no-counterexample",
          "Exact, w = (3,1,1): P(consensus 0 from empty) >= 1/3 + 2/100",
          k72_exact_direction(3)),
    Check("K72.c/exact-residual-symmetry", "K72.c", "proves", "witness", "no-counterexample",
          "Exact, r = 2 and 3: consensus 1 and consensus 2 have equal probability, so explicit breaking leaves Sym(F minus the cheap form)",
          k72_exact_residual),
    Check("K72.c/exact-monotone", "K72.c", "proves", "witness", "no-counterexample",
          "Exact: P(consensus 0) is nondecreasing across r = 1, 2, 3",
          k72_exact_monotone),

    Check("K71.ensemble/converged", "K71.ensemble", "probe", "witness", "no-counterexample",
          "Simulation, 20 agents, 5 forms, 2000 seeds per configuration, 50000 interactions: converged fraction >= 0.99 in each of r = 1, 2, 3 (K71 c); thresholds fixed in gauge.md Part A",
          sim_converged),
    Check("K71.ensemble/control-symmetric", "K71.ensemble", "probe", "witness", "no-counterexample",
          "Simulation, r = 1: max over forms of |share - 1/5| <= 0.036 (K71 b); fixed in gauge.md Part A",
          sim_control_symmetric),
    Check("K72.c/sim-cheaper-favored-r2", "K72.c", "probe", "witness", "no-counterexample",
          "Simulation, r = 2: share of the cheap form >= 1/5 + 0.036; fixed in gauge.md Part A",
          sim_cheaper_favored(1)),
    Check("K72.c/sim-cheaper-favored-r3", "K72.c", "probe", "witness", "no-counterexample",
          "Simulation, r = 3: share of the cheap form >= 1/5 + 0.036; fixed in gauge.md Part A",
          sim_cheaper_favored(2)),
    Check("K72.c/sim-monotone", "K72.c", "probe", "witness", "no-counterexample",
          "Simulation: share(r = 3) - share(r = 2) >= -0.036; fixed in gauge.md Part A",
          sim_monotone),
    Check("K72.c/sim-residual-symmetry", "K72.c", "probe", "witness", "no-counterexample",
          "Simulation, r = 2 and 3: the four other forms' shares are within 0.040 of equal; fixed in gauge.md Part A",
          sim_residual),
]
