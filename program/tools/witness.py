"""Exact counterexample witnesses for information inequalities.

A refutation needs a concrete distribution, re-checked by code independent of the prover
(harness.md §5.2). A Dist is a finite joint pmf with Fraction weights. Its hypothesis tests
(independence, functional dependence) are exact. Mutual information is a float; a witness
counts only if the violated inequality misses by more than TOL.
"""
import itertools
import math
from fractions import Fraction

TOL = 1e-9


def _vars(spec):
    if isinstance(spec, str):
        return tuple(v.strip() for v in spec.split(",") if v.strip())
    return tuple(spec)


class Dist:
    def __init__(self, pmf):
        """pmf: {tuple of (name, value) pairs, sorted by name: Fraction}"""
        self.pmf = pmf
        total = sum(pmf.values())
        if total != 1:
            raise ValueError(f"pmf sums to {total}, not 1")

    @classmethod
    def uniform(cls, f, **ranges):
        """Uniform over the product of `ranges`; f(**point) returns {name: value} for every variable."""
        names = sorted(ranges)
        points = list(itertools.product(*(ranges[n] for n in names)))
        pmf = {}
        for pt in points:
            row = tuple(sorted(f(**dict(zip(names, pt))).items()))
            pmf[row] = pmf.get(row, 0) + Fraction(1, len(points))
        return cls(pmf)

    def marg(self, spec):
        vs = _vars(spec)
        out = {}
        for row, p in self.pmf.items():
            d = dict(row)
            key = tuple(d[v] for v in vs)
            out[key] = out.get(key, 0) + p
        return out

    def H(self, spec):
        return -sum(float(p) * math.log2(p) for p in self.marg(spec).values() if p > 0)

    def I(self, a, b, given=()):
        a, b, c = _vars(a), _vars(b), _vars(given)
        return self.H(a + c) + self.H(b + c) - self.H(a + b + c) - (self.H(c) if c else 0.0)

    def indep(self, a, b, given=()):
        """Exact: p(a,b,c) p(c) == p(a,c) p(b,c) for every outcome."""
        a, b, c = _vars(a), _vars(b), _vars(given)
        pabc, pac, pbc = self.marg(a + b + c), self.marg(a + c), self.marg(b + c)
        pc = self.marg(c) if c else {(): Fraction(1)}
        na, nb = len(a), len(b)
        for xa in {k[:na] for k in pac}:
            for xb in {k[:nb] for k in pbc}:
                for xc in pc:
                    lhs = pabc.get(xa + xb + xc, 0) * pc[xc]
                    if lhs != pac.get(xa + xc, 0) * pbc.get(xb + xc, 0):
                        return False
        return True

    def determines(self, x, y):
        """Exact: y is a function of x on the support."""
        x, y = _vars(x), _vars(y)
        seen = {}
        for key in self.marg(x + y):
            if seen.setdefault(key[:len(x)], key[len(x):]) != key[len(x):]:
                return False
        return True


def verdict(hypotheses, gap):
    """hypotheses: {description: bool}, checked exactly. gap: lhs - rhs of the claimed `lhs <= rhs`.
    Returns (result, detail)."""
    failed = [h for h, ok in hypotheses.items() if not ok]
    if failed:
        return "no-counterexample", {"failed_hypotheses": failed, "gap": round(gap, 12)}
    if gap > TOL:
        return "counterexample", {"hypotheses": sorted(hypotheses), "gap": round(gap, 12)}
    return "no-counterexample", {"gap": round(gap, 12)}
