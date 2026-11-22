"""Naming game for K71 and K72(c): conventions as spontaneous symmetry breaking (S-02, check 4).

The game and its parameters are fixed in program/checks/gauge.md, Part A, which was committed
before this file existed. A population state is a tuple of inventories, each a bitmask over the
form set F = {0, ..., m-1}. `speak` and `hear` are the whole update rule. The exact chain
(`transitions`) and the simulator (`run`) both use them, so they cannot drift apart.

Symmetry: relabeling forms by a permutation s of F, applied to every inventory, commutes with
the update exactly when the weights w are s-invariant. Weights w_f > 0 are the relative
propensities to produce form f. Lowering the cost of one form raises its weight.
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction
from itertools import accumulate


def speak(mask: int, w) -> list[tuple[int, object]]:
    """Candidate (form, weight) pairs for a speaker holding `mask`. An empty inventory invents over all forms."""
    forms = [f for f in range(len(w)) if mask >> f & 1] or list(range(len(w)))
    return [(f, w[f]) for f in forms]


def hear(speaker: int, hearer: int, f: int) -> tuple[int, int, bool]:
    """Both inventories after the speaker says f. Success collapses both to {f}; failure teaches the hearer."""
    if hearer >> f & 1:
        return 1 << f, 1 << f, True
    return speaker | 1 << f, hearer | 1 << f, False


def relabel(state: tuple[int, ...], s: tuple[int, ...]) -> tuple[int, ...]:
    """Apply the permutation s of forms (form f becomes s[f]) to every inventory; the result is a sorted multiset."""
    out = []
    for mask in state:
        new = 0
        for f, g in enumerate(s):
            if mask >> f & 1:
                new |= 1 << g
        out.append(new)
    return tuple(sorted(out))


# Exact chain ----------------------------------------------------------------------------------
# Agents are anonymous and pairs are drawn uniformly, so a state is the sorted multiset of inventories.

def transitions(state: tuple[int, ...], w) -> dict[tuple[int, ...], Fraction]:
    """Exact one-step law from `state`; `w` holds ints or Fractions."""
    M = len(state)
    out: dict[tuple[int, ...], Fraction] = {}
    for i, j in itertools.permutations(range(M), 2):
        cands = speak(state[i], w)
        total = sum(wt for _, wt in cands)
        for f, wt in cands:
            si, sj, _ = hear(state[i], state[j], f)
            nxt = list(state)
            nxt[i], nxt[j] = si, sj
            key = tuple(sorted(nxt))
            out[key] = out.get(key, Fraction(0)) + Fraction(1, M * (M - 1)) * Fraction(wt) / Fraction(total)
    return out


def all_states(M: int, m: int) -> list[tuple[int, ...]]:
    return list(itertools.combinations_with_replacement(range(2 ** m), M))


def consensus_states(M: int, m: int) -> list[tuple[int, ...]]:
    return [tuple([1 << f] * M) for f in range(m)]


def kernel(M: int, m: int, w) -> dict[tuple[int, ...], dict[tuple[int, ...], Fraction]]:
    """Transition law from every multiset state, reachable or not."""
    return {s: transitions(s, w) for s in all_states(M, m)}


def step_law(law: dict, T: dict) -> dict:
    out: dict = {}
    for s, p in law.items():
        for s2, q in T[s].items():
            out[s2] = out.get(s2, Fraction(0)) + p * q
    return out


def absorption(T: dict, M: int, m: int) -> dict[tuple[int, ...], list[Fraction]]:
    """For every state, the probability of absorption into each consensus state (exact Gaussian elimination).

    Raises if the system is singular, which happens exactly when a recurrent class other than the
    consensus states exists.
    """
    goal = consensus_states(M, m)
    rest = [s for s in T if s not in goal]
    idx = {s: n for n, s in enumerate(rest)}
    n = len(rest)
    # Solve (I - Q) h = R for each target at once; columns are the m targets.
    A = [[Fraction(0)] * (n + m) for _ in range(n)]
    for s in rest:
        r = idx[s]
        A[r][r] += 1
        for s2, p in T[s].items():
            if s2 in idx:
                A[r][idx[s2]] -= p
            else:
                A[r][n + goal.index(s2)] += p
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            raise ValueError("singular: a recurrent class other than the consensus states exists")
        A[c], A[piv] = A[piv], A[c]
        inv = 1 / A[c][c]
        A[c] = [x * inv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                fac = A[r][c]
                A[r] = [x - fac * y for x, y in zip(A[r], A[c])]
    out = {s: [A[idx[s]][n + k] for k in range(m)] for s in rest}
    for k, g in enumerate(goal):
        out[g] = [Fraction(int(k == c)) for c in range(m)]
    return out


# Simulation -----------------------------------------------------------------------------------

def weights(m: int, r: float) -> list[float]:
    """Form 0 has relative weight r (cost c = -ln r below the rest); r = 1 is the symmetric game."""
    return [float(r)] + [1.0] * (m - 1)


def make_picker(w):
    cache: dict[int, tuple[list[int], list[float]]] = {}

    def pick(mask: int, rng: random.Random) -> int:
        c = cache.get(mask)
        if c is None:
            cands = speak(mask, w)
            c = ([f for f, _ in cands], list(accumulate(wt for _, wt in cands)))
            cache[mask] = c
        forms, cum = c
        x = rng.random() * cum[-1]
        for f, cw in zip(forms, cum):
            if x < cw:
                return f
        return forms[-1]

    return pick


def run(M: int, w, T_max: int, seed: int) -> tuple[int | None, int]:
    """One game from the empty state. Returns (convention or None, interactions used)."""
    rng = random.Random(seed)
    pick = make_picker(w)
    inv = [0] * M
    for t in range(1, T_max + 1):
        i = rng.randrange(M)
        j = rng.randrange(M - 1)
        j += j >= i
        f = pick(inv[i], rng)
        inv[i], inv[j], ok = hear(inv[i], inv[j], f)
        if ok and all(x == inv[i] for x in inv):
            return f, t
    return None, T_max


def ensemble(M: int, m: int, r: float, R: int, T_max: int, config: int) -> dict:
    """R independent games, seeds 10000 * config + i. Counts of conventions, plus convergence times."""
    w = weights(m, r)
    counts = [0] * m
    times = []
    for i in range(R):
        f, t = run(M, w, T_max, 10000 * config + i)
        if f is not None:
            counts[f] += 1
            times.append(t)
    return {"counts": counts, "converged": sum(counts), "R": R, "mean_time": sum(times) / max(len(times), 1),
            "max_time": max(times, default=0)}
