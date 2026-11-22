"""PSITIP pilot: Shannon-type checks of core program claims.

Usage: python3 -I program/proofs/psitip/pilot.py /path/to/psitip   (a clone of github.com/cheuktingli/psitip)
Needs: numpy scipy sympy ortools lark-parser pylatexenc. PSITIP is GPL-3.0; it is not vendored here.
Results and interpretation: program/proofs/psitip/RESULTS.md
"""
import sys, itertools, math
sys.path.insert(0, sys.argv[1])
from psitip import *
PsiOpts.setting(solver="ortools.GLOP")

W, D, C, xi, E, T, Da, Db, Xa, Xb, W0, W1 = rv("W", "D", "C", "xi", "E", "T", "Da", "Db", "Xa", "Xb", "W0", "W1")
def ci(a, b, given=None):  # conditional independence a ⊥ b | given
    return (I(a & b | given) == 0) if given is not None else (I(a & b) == 0)
def fn(y, x):              # y is a function of x
    return H(y | x) == 0

checks = [
  ("SANITY  unconstrained I(W;D) <= 0  [expect False]", H(W) >= 0, I(W & D) <= 0),
  ("GM-T2   W1=F(W0,xi), xi ⊥ W | W0  =>  I(W;W1) <= I(W;W0)", fn(W1, W0 + xi) & ci(xi, W, W0), I(W & W1) <= I(W & W0)),
  ("GM-T4.1 C=f(D,E)  =>  I(W;D,C) >= I(W;D)", fn(C, D + E) & ci(E, D, W), I(W & D + C) >= I(W & D)),
  ("GM-T4.1 with NO hypotheses  =>  I(W;D,C) >= I(W;D)  [hypothesis-ablation check]", H(W) >= 0, I(W & D + C) >= I(W & D)),
  ("GM-T4.2 as written: C=f(D,xi), xi ⊥ W  =>  I(W;D,C) <= I(W;D)  [expect not provable]", fn(C, D + xi) & ci(xi, W), I(W & D + C) <= I(W & D)),
  ("GM-T4.2 corrected: xi ⊥ W | D  =>  I(W;D,C) <= I(W;D)", fn(C, D + xi) & ci(xi, W, D), I(W & D + C) <= I(W & D)),
  ("GM-T4.2 corrected, replacement: xi ⊥ W | D  =>  I(W;C) <= I(W;D)", fn(C, D + xi) & ci(xi, W, D), I(W & C) <= I(W & D)),
  ("GM-T4.2 with xi ⊥ (W,D)  =>  I(W;D,C) <= I(W;D)", fn(C, D + xi) & ci(xi, W + D), I(W & D + C) <= I(W & D)),
  ("OUT-S26 Da-W-Db, Xa<-Da, Xb<-Db  =>  I(Xa;Xb) <= I(Da;Db)",
     ci(Da, Db, W) & ci(Xa, W + Db + Xb, Da) & ci(Xb, W + Da, Db), I(Xa & Xb) <= I(Da & Db)),
  ("OUT-S26 same  =>  I(Da;Db) <= I(W;Da)",
     ci(Da, Db, W) & ci(Xa, W + Db + Xb, Da) & ci(Xb, W + Da, Db), I(Da & Db) <= I(W & Da)),
  ("OUT-S26 WITHOUT Da ⊥ Db | W  =>  I(Xa;Xb) <= I(W;Da)  [expect not provable]",
     ci(Xa, W + Db + Xb, Da) & ci(Xb, W + Da, Db), I(Xa & Xb) <= I(W & Da)),
  ("MR1     T depends on W only via (D,E)  =>  I(W;T) <= I(W;D) + I(W;E|D)", ci(W, T, D + E), I(W & T) <= I(W & D) + I(W & E | D)),
  ("MR1     same, no verifier term  =>  I(W;T) <= I(W;D)  [expect not provable]", ci(W, T, D + E), I(W & T) <= I(W & D)),
]
results = []
for name, hyp, concl in checks:
    try:
        ok = bool(hyp >> concl)
    except Exception as e:
        ok = f"ERROR {e}"
    results.append((name, ok)); print(f"{str(ok):6}  {name}", flush=True)

# Independent numeric check of the T4.2 counterexample (no psitip): W, D fair bits, xi = W xor D, C = D xor xi.
def MI(pxy):
    px, py = {}, {}
    for (x, y), p in pxy.items(): px[x] = px.get(x, 0) + p; py[y] = py.get(y, 0) + p
    return sum(p * math.log2(p / (px[x] * py[y])) for (x, y), p in pxy.items() if p > 0)
joint = {}
for w, d in itertools.product([0, 1], repeat=2):
    x = w ^ d; c = d ^ x; joint[(w, d, x, c)] = 0.25
def marg(f):
    out = {}
    for k, p in joint.items(): key = f(*k); out[key] = out.get(key, 0) + p
    return out
print("NUMERIC xor example: I(xi;W) =", MI(marg(lambda w,d,x,c: (x, w))),
      " I(W;D) =", MI(marg(lambda w,d,x,c: (w, d))),
      " I(W;D,C) =", MI(marg(lambda w,d,x,c: (w, (d, c)))))
