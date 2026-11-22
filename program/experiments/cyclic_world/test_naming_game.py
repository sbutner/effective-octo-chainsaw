import itertools
from fractions import Fraction

import naming_game as ng

M, m = 3, 3
PERMS = list(itertools.permutations(range(m)))
EMPTY = (0,) * M


def compose(a, b):
    """(b after a)[f] = b[a[f]]"""
    return tuple(b[a[f]] for f in range(len(a)))


def equivariant(T, p):
    return all({ng.relabel(s2, p): q for s2, q in row.items()} == T[ng.relabel(s, p)] for s, row in T.items())


def test_hear_success_collapses_and_failure_teaches():
    assert ng.hear(0b001, 0b011, 0) == (0b001, 0b001, True)
    assert ng.hear(0b001, 0b010, 0) == (0b001, 0b011, False)
    assert ng.hear(0b000, 0b100, 1) == (0b010, 0b110, False)  # an invented form joins the speaker's inventory


def test_speak_empty_inventory_invents_over_all_forms():
    assert [f for f, _ in ng.speak(0, [1, 1, 1])] == [0, 1, 2]
    assert [f for f, _ in ng.speak(0b101, [1, 1, 1])] == [0, 2]


def test_relabel_is_a_group_action():
    state = (0b001, 0b011, 0b110)
    for a, b in itertools.product(PERMS, PERMS):
        assert ng.relabel(ng.relabel(state, a), b) == ng.relabel(state, compose(a, b))
    assert ng.relabel(state, (0, 1, 2)) == tuple(sorted(state))


def test_rows_sum_to_one_and_agents_stay_anonymous():
    T = ng.kernel(M, m, [1, 1, 1])
    assert len(T) == 120
    assert all(sum(row.values()) == 1 for row in T.values())
    assert all(list(s2) == sorted(s2) for row in T.values() for s2 in row)


def test_kernel_is_equivariant_for_equal_weights_exactly():
    T = ng.kernel(M, m, [1, 1, 1])
    assert all(equivariant(T, p) for p in PERMS)


def test_biased_kernel_is_equivariant_only_under_the_stabilizer_of_the_weights():
    T = ng.kernel(M, m, [2, 1, 1])
    assert equivariant(T, (0, 2, 1))        # swaps forms 1 and 2: fixes the weights
    assert not equivariant(T, (1, 0, 2))    # moves the cheap form
    assert not equivariant(T, (1, 2, 0))


def test_absorbing_states_are_exactly_the_consensus_states():
    T = ng.kernel(M, m, [1, 1, 1])
    absorbing = sorted(s for s, row in T.items() if row == {s: 1})
    assert absorbing == sorted(ng.consensus_states(M, m))


def test_absorption_is_certain_and_uniform_from_the_empty_state():
    h = ng.absorption(ng.kernel(M, m, [1, 1, 1]), M, m)
    assert h[EMPTY] == [Fraction(1, 3)] * 3
    assert all(sum(v) == 1 for v in h.values())


def test_cheaper_form_is_favored_exactly_and_the_others_stay_equal():
    h = ng.absorption(ng.kernel(M, m, [2, 1, 1]), M, m)[EMPTY]
    assert sum(h) == 1 and h[0] > Fraction(1, 3) and h[1] == h[2]


def test_run_is_deterministic_in_the_seed_and_converges():
    w = ng.weights(3, 1.0)
    a = ng.run(5, w, 20000, seed=7)
    assert a == ng.run(5, w, 20000, seed=7)
    assert a[0] in (0, 1, 2) and a[1] < 20000


def test_budget_exhaustion_reports_no_convention():
    assert ng.run(20, ng.weights(5, 1.0), 3, seed=1) == (None, 3)


def test_ensemble_is_reproducible_and_counts_every_converged_run():
    e1 = ng.ensemble(6, 3, 1.0, 10, 20000, config=0)
    assert e1 == ng.ensemble(6, 3, 1.0, 10, 20000, config=0)
    assert e1["converged"] == sum(e1["counts"]) == 10
