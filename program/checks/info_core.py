"""Information-theoretic core: GM T2, T4.1, T4.2, OUT-S26 and MR1.

Migrated from the PSITIP pilot of 2026-11-22. Variables: W = Omega (the world), D = corpus,
C = commentary, xi = noise, E = verifier or independent evidence, T = model output (Theta, Y),
Da, Db, Xa, Xb = two agents' data and representations. Hand proofs and findings: info_core.md.

PSITIP `provable` is sound. `not-provable` means no Shannon-type proof exists, never that the
inequality is false; that takes a witness.
"""
from check import Check
from witness import Dist


def ci(p, a, b, given=None):
    return (p.I(a & b | given) == 0) if given is not None else (p.I(a & b) == 0)


def fn(p, y, x):
    return p.H(y | x) == 0


def t42_written(p):
    W, D, C, xi = p.rv("W", "D", "C", "xi")
    return fn(p, C, D + xi) & ci(p, xi, W), p.I(W & D + C) <= p.I(W & D)


def t42_corrected(conclusion):
    def run(p):
        W, D, C, xi = p.rv("W", "D", "C", "xi")
        lhs = p.I(W & D + C) if conclusion == "joint" else p.I(W & C)
        return fn(p, C, D + xi) & ci(p, xi, W, D), lhs <= p.I(W & D)
    return run


def t42_indep_wd(p):
    W, D, C, xi = p.rv("W", "D", "C", "xi")
    return fn(p, C, D + xi) & ci(p, xi, W + D), p.I(W & D + C) <= p.I(W & D)


def s26(drop_channel_ci, conclusion):
    def run(p):
        W, Da, Db, Xa, Xb = p.rv("W", "Da", "Db", "Xa", "Xb")
        hyp = ci(p, Xa, W + Db + Xb, Da) & ci(p, Xb, W + Da, Db)
        if not drop_channel_ci:
            hyp = hyp & ci(p, Da, Db, W)
        concl = {"Xa;Xb<=Da;Db": p.I(Xa & Xb) <= p.I(Da & Db),
                 "Da;Db<=W;Da": p.I(Da & Db) <= p.I(W & Da),
                 "Xa;Xb<=W;Da": p.I(Xa & Xb) <= p.I(W & Da)}[conclusion]
        return hyp, concl
    return run


def mr1(verifier_term):
    def run(p):
        W, D, E, T = p.rv("W", "D", "E", "T")
        rhs = p.I(W & D) + p.I(W & E | D) if verifier_term else p.I(W & D)
        return ci(p, W, T, D + E), p.I(W & T) <= rhs
    return run


def sanity(p):
    W, D = p.rv("W", "D")
    return p.H(W) >= 0, p.I(W & D) <= 0


def t2(p):
    W, W0, W1, xi = p.rv("W", "W0", "W1", "xi")
    return fn(p, W1, W0 + xi) & ci(p, xi, W, W0), p.I(W & W1) <= p.I(W & W0)


def t41(with_hypotheses):
    def run(p):
        W, D, C, E = p.rv("W", "D", "C", "E")
        hyp = fn(p, C, D + E) & ci(p, E, D, W) if with_hypotheses else p.H(W) >= 0
        return hyp, p.I(W & D + C) >= p.I(W & D)
    return run


def t42_xor():
    """W, D independent fair bits; xi = W xor D; C = D xor xi = W."""
    d = Dist.uniform(lambda W, D: {"W": W, "D": D, "xi": W ^ D, "C": W}, W=[0, 1], D=[0, 1])
    hyps = {"C = f(D, xi)": d.determines("D,xi", "C"), "xi ⊥ W": d.indep("xi", "W")}
    return hyps, d.I("W", "D,C") - d.I("W", "D")


def s26_shared_bit():
    """Da = Db = Xa = Xb = B, a fair bit independent of W: agreement with no grounding."""
    d = Dist.uniform(lambda W, B: {"W": W, "Da": B, "Db": B, "Xa": B, "Xb": B}, W=[0, 1], B=[0, 1])
    hyps = {"Xa ⊥ (W,Db,Xb) | Da": d.indep("Xa", "W,Db,Xb", "Da"),
            "Xb ⊥ (W,Da) | Db": d.indep("Xb", "W,Da", "Db")}
    return hyps, d.I("Xa", "Xb") - d.I("W", "Da")


def mr1_constant_corpus():
    """D constant, T = E = W: all information reaches T through the verifier."""
    d = Dist.uniform(lambda W: {"W": W, "D": 0, "E": W, "T": W}, W=[0, 1])
    hyps = {"W ⊥ T | (D,E)": d.indep("W", "T", "D,E")}
    return hyps, d.I("W", "T") - d.I("W", "D")


CHECKS = [
    Check("psitip/sanity", None, "sanity", "psitip", "not-provable",
          "Unconstrained I(W;D) <= 0 must not be provable", sanity),

    Check("GM-T2/main", "GM-T2", "proves", "psitip", "provable",
          "W1 = F(W0, xi), xi ⊥ W | W0  =>  I(W;W1) <= I(W;W0)", t2),

    Check("GM-T4.1.inequality/main", "GM-T4.1.inequality", "proves", "psitip", "provable",
          "C = f(D, E), E ⊥ D | W  =>  I(W;D,C) >= I(W;D)", t41(True)),
    Check("GM-T4.1.inequality/ablate-all", "GM-T4.1.inequality", "probe", "psitip", "provable",
          "No hypotheses  =>  I(W;D,C) >= I(W;D): the hypotheses are unused", t41(False)),

    Check("GM-T4.2/psitip", "GM-T4.2", "probe", "psitip", "not-provable",
          "As written: C = f(D, xi), xi ⊥ W  =>  I(W;D,C) <= I(W;D)", t42_written),
    Check("GM-T4.2/xor", "GM-T4.2", "refutes", "witness", "counterexample",
          "XOR: W, D fair bits, xi = W xor D, C = W satisfies the hypotheses with I(W;D,C) - I(W;D) = 1",
          t42_xor),
    Check("GM-T4.2~cond-D/joint", "GM-T4.2~cond-D", "proves", "psitip", "provable",
          "Corrected: C = f(D, xi), xi ⊥ W | D  =>  I(W;D,C) <= I(W;D)", t42_corrected("joint")),
    Check("GM-T4.2~cond-D/replacement", "GM-T4.2~cond-D", "proves", "psitip", "provable",
          "Corrected, replacement clause: same hypotheses  =>  I(W;C) <= I(W;D)", t42_corrected("single")),
    Check("GM-T4.2~indep-WD/joint", "GM-T4.2~indep-WD", "proves", "psitip", "provable",
          "Fully independent noise: C = f(D, xi), xi ⊥ (W,D)  =>  I(W;D,C) <= I(W;D)", t42_indep_wd),

    Check("OUT-S26/first-link", "OUT-S26", "proves", "psitip", "provable",
          "Da ⊥ Db | W; Xa ⊥ (W,Db,Xb) | Da; Xb ⊥ (W,Da) | Db  =>  I(Xa;Xb) <= I(Da;Db)",
          s26(False, "Xa;Xb<=Da;Db")),
    Check("OUT-S26/second-link", "OUT-S26", "proves", "psitip", "provable",
          "Same hypotheses  =>  I(Da;Db) <= I(W;Da)", s26(False, "Da;Db<=W;Da")),
    Check("OUT-S26/ablate-channel-ci", "OUT-S26", "probe", "psitip", "not-provable",
          "Without Da ⊥ Db | W  =>  I(Xa;Xb) <= I(W;Da)", s26(True, "Xa;Xb<=W;Da")),
    Check("OUT-S26/ablate-channel-ci-witness", "OUT-S26", "probe", "witness", "counterexample",
          "Shared bit: Da = Db = Xa = Xb = B ⊥ W breaks the ablated bound, so Da ⊥ Db | W is load-bearing",
          s26_shared_bit),

    Check("MR1/main", "MR1", "proves", "psitip", "provable",
          "W ⊥ T | (D,E)  =>  I(W;T) <= I(W;D) + I(W;E|D)", mr1(True)),
    Check("MR1/ablate-verifier", "MR1", "probe", "psitip", "not-provable",
          "Same hypothesis  =>  I(W;T) <= I(W;D), without the verifier term", mr1(False)),
    Check("MR1/ablate-verifier-witness", "MR1", "probe", "witness", "counterexample",
          "D constant, T = E = W breaks the bound without the verifier term, so the term is load-bearing",
          mr1_constant_corpus),
]
