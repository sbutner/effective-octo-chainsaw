import numpy as np
import pytest

from cyclic_world import Channel, Episode, World, corpus_profile, grounded_information, make_agent, run


# S4 ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("N", [12, 24])
@pytest.mark.parametrize("s", [0.0, 0.2, 0.5, 0.9, 1.0])
def test_s4_coefficients_scale(N, s):
    w = World(N)
    F = np.fft.fft(w.f)
    C = np.fft.fft(corpus_profile(w, s))
    k = np.arange(N)
    np.testing.assert_allclose(C, (1 - s + s * (-1.0) ** k) * F, atol=1e-12)


@pytest.mark.parametrize("N", [12, 24])
def test_s4_odd_vanish_at_half_before_and_after_log(N):
    w = World(N)
    p = corpus_profile(w, 0.5)
    for arr in (p, np.log(p)):
        assert np.abs(np.fft.fft(arr)[1::2]).max() < 1e-12
    assert np.abs(np.fft.fft(w.f)[1::2]).max() > 0.1  # default profile does have odd harmonics
    assert np.abs(np.fft.fft(w.f)[2]) > 0.1           # and a semiannual one


def test_s4_odd_N_rejected():
    with pytest.raises(ValueError):
        corpus_profile(World(7), 0.5)


# S18 --------------------------------------------------------------------------------------
def test_s18_box_gains_match_outline():
    g = Channel.box_blur(12, 3).gains()
    assert [round(float(x), 2) for x in g[1:6]] == [0.91, 0.67, 0.33, 0.00, 0.24]
    assert g[0] == pytest.approx(1.0)
    k = np.arange(1, 6)
    np.testing.assert_allclose(g[1:6], np.abs(np.sin(np.pi * k / 4) / (3 * np.sin(np.pi * k / 12))), atol=1e-12)


def test_s18_two_readers_agree_at_k0_and_diverge_at_high_harmonics():
    # Reader A sees f unblurred; reader B sees f through the width-3 blur (circular convolution).
    # Divergence at harmonic k is 1 - |B_k|/|A_k| = 1 - gain_k.
    N = 12
    # Default profile has only harmonics 0..2, so use a profile with energy at every harmonic.
    w = World(N, np.random.default_rng(0).uniform(1.0, 2.0, N))
    box = Channel.box_blur(N, 3).K[0]
    seen_B = np.real(np.fft.ifft(np.fft.fft(w.f) * np.fft.fft(box)))
    FA, FB = np.fft.fft(w.f), np.fft.fft(seen_B)
    assert abs(FA[0] - FB[0]) < 1e-12  # agree on k=0
    div = 1 - np.abs(FB[1:7]) / np.abs(FA[1:7])  # k = 1..6
    # The outline says "agree below, diverge above". The gains are not monotone (k=5 beats k=4),
    # so assert the band statement: each of k=3..6 diverges more than each of k=1..2, peak at k=4.
    assert div[2:].min() > div[:2].max()
    assert int(np.argmax(div)) + 1 == 4


# Runs -------------------------------------------------------------------------------------
@pytest.mark.parametrize("A", [1, 2, 7])
@pytest.mark.parametrize("N", [12, 7, 365])
def test_run_many_agents_reproducible(N, A):
    w = World(N)
    chans = [Channel.noiseless(N), Channel.box_blur(N, 3), Channel.constant(N)]
    agents = [make_agent(i, w, south=bool(i % 2), sensorium=chans[i % 3]) for i in range(A)]
    T = 2 * N
    r1 = run(w, agents, T, np.random.default_rng(5))
    r2 = run(w, agents, T, np.random.default_rng(5))
    assert r1 == r2 and set(r1) == set(range(A))
    for a in agents:
        eps = r1[a.id]
        assert len(eps) == T and all(isinstance(e, Episode) for e in eps)
        assert all(e.k is None and e.m is None and e.u is None for e in eps)
        if a.sensorium is chans[0]:  # noiseless: observes its own local phase exactly
            assert [e.x for e in eps] == [(t + a.offset) % N for t in range(T)]


def test_run_seed_changes_noisy_stream():
    w = World(12)
    a = [make_agent(0, w, False, Channel.constant(12))]
    assert run(w, a, 50, np.random.default_rng(1)) != run(w, a, 50, np.random.default_rng(2))


def test_hemispheres_offset_by_half():
    w = World(12)
    a = [make_agent(0, w, False, Channel.noiseless(12)), make_agent(1, w, True, Channel.noiseless(12))]
    r = run(w, a, 12, np.random.default_rng(0))
    assert all((r[1][t].x - r[0][t].x) % 12 == 6 for t in range(12))


# Grounded information -----------------------------------------------------------------------
@pytest.mark.parametrize("N", [12, 7, 365])
def test_info_noiseless_and_constant(N):
    p = np.full(N, 1 / N)
    assert grounded_information(p, Channel.noiseless(N).K) == pytest.approx(np.log2(N), abs=1e-12)
    assert grounded_information(p, Channel.constant(N).K) == pytest.approx(0.0, abs=1e-12)


def test_info_equivariant_under_shift():
    rng = np.random.default_rng(3)
    N = 12
    prior = rng.random(N)
    prior /= prior.sum()
    K = rng.random((N, N))
    K /= K.sum(1, keepdims=True)
    base = grounded_information(prior, K)
    for g in range(N):
        p2 = np.roll(prior, g)                          # p2[w+g] = p[w]
        K2 = np.roll(np.roll(K, g, axis=0), g, axis=1)  # K2[w+g, o+g] = K[w, o]
        assert grounded_information(p2, K2) == pytest.approx(base, abs=1e-12)
        assert grounded_information(p2, np.roll(K, g, axis=0)) == pytest.approx(base, abs=1e-12)
    assert 0 < grounded_information(prior, Channel.box_blur(N, 3).K) < np.log2(N)


def test_info_invariant_under_the_whole_dihedral_group():
    """K70: I(Omega; X) under P equals I(Omega; X o g^-1) under g P, for every g in D_N (rotations and reflections)."""
    rng = np.random.default_rng(4)
    N = 12
    prior = rng.random(N)
    prior /= prior.sum()
    K = rng.random((N, N))
    K /= K.sum(1, keepdims=True)
    base = grounded_information(prior, K)
    for g in range(N):
        for sign in (1, -1):
            perm = np.array([(sign * w + g) % N for w in range(N)])  # w -> perm[w], a bijection of Z_N
            p2 = np.empty(N)
            p2[perm] = prior                  # (g P)(perm[w]) = P(w)
            K2 = np.empty_like(K)
            K2[perm] = K                      # (X o g^-1)(. | perm[w]) = X(. | w)
            assert grounded_information(p2, K2) == pytest.approx(base, abs=1e-12)
            if sign == -1:
                assert not np.allclose(p2, prior)  # a reflection really moves the law
