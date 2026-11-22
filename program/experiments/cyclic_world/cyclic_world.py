"""Cyclic-world testbed, rung R0. World, channels, agents, episodes, exact grounded information."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


def default_profile(N: int) -> np.ndarray:
    """Smooth annual cycle plus a semiannual harmonic, strictly positive."""
    w = np.arange(N) / N
    return 1.0 + 0.5 * np.cos(2 * np.pi * (w - 0.1)) + 0.3 * np.cos(4 * np.pi * (w - 0.05))


@dataclass(frozen=True)
class World:
    """Primitive 1: process omega_t = t mod N on Z_N, symmetry G = Z_N acting by shift."""
    N: int
    f: np.ndarray = field(default=None, compare=False)

    def __post_init__(self):
        f = default_profile(self.N) if self.f is None else np.asarray(self.f, float)
        if f.shape != (self.N,) or (f <= 0).any():
            raise ValueError("profile must be positive with length N")
        object.__setattr__(self, "f", f)

    def state(self, t: int) -> int:
        return t % self.N

    def act(self, g: int, w: int) -> int:
        return (w + g) % self.N


@dataclass(frozen=True)
class Channel:
    """Primitive 2: Markov kernel K[omega, o] with a time and an energy cost per use."""
    K: np.ndarray = field(compare=False)
    time_cost: float = 0.0
    energy_cost: float = 0.0

    def __post_init__(self):
        K = np.asarray(self.K, float)
        if K.ndim != 2 or (K < 0).any() or not np.allclose(K.sum(1), 1.0):
            raise ValueError("K must be row-stochastic")
        object.__setattr__(self, "K", K)

    @staticmethod
    def noiseless(N: int, **costs) -> "Channel":
        return Channel(np.eye(N), **costs)

    @staticmethod
    def constant(N: int, **costs) -> "Channel":
        return Channel(np.full((N, N), 1.0 / N), **costs)

    @staticmethod
    def box_blur(N: int, w: int, **costs) -> "Channel":
        """Observe a uniform draw from w consecutive phases, from omega - w//2 to omega - w//2 + w - 1 (centred on omega for odd w)."""
        if not 1 <= w <= N:
            raise ValueError("need 1 <= w <= N")
        K = np.zeros((N, N))
        for a in range(N):
            for j in range(w):
                K[a, (a + j - w // 2) % N] += 1.0 / w
        return Channel(K, **costs)

    def gains(self) -> np.ndarray:
        """|k-th DFT coefficient| of the kernel row at phase 0, k = 0..N-1 (shift-invariant kernels)."""
        return np.abs(np.fft.fft(self.K[0]))


@dataclass(frozen=True)
class Agent:
    """Primitive 3 (R0 shell): id, hemisphere offset, sensorium channel."""
    id: int
    offset: int
    sensorium: Channel


def make_agent(id: int, world: World, south: bool, sensorium: Channel) -> Agent:
    return Agent(id, world.N // 2 if south else 0, sensorium)


@dataclass(frozen=True)
class Episode:
    """e_t = (x, k, m, u). k, m, u stay None until R1/R2. Here x is the observed local phase."""
    t: int
    x: Any
    k: Any = None
    m: Any = None
    u: Any = None


def run(world: World, agents: list[Agent], T: int, rng: np.random.Generator) -> dict[int, list[Episode]]:
    """Each agent at time t draws o ~ K[(omega_t + offset) mod N, .]. Deterministic given rng."""
    streams: dict[int, list[Episode]] = {a.id: [] for a in agents}
    cdfs = {a.id: np.cumsum(a.sensorium.K, axis=1) for a in agents}
    for t in range(T):
        w = world.state(t)
        for a in agents:
            cdf = cdfs[a.id][(w + a.offset) % world.N]
            o = int(min(np.searchsorted(cdf, rng.random(), side="right"), len(cdf) - 1))
            streams[a.id].append(Episode(t=t, x=o))
    return streams


def corpus_profile(world: World, s: float) -> np.ndarray:
    """(1-s) f(w) + s f(w + N/2); needs even N."""
    if world.N % 2:
        raise ValueError("the hemisphere shift N/2 needs even N")
    return (1 - s) * world.f + s * np.roll(world.f, -(world.N // 2))


def grounded_information(prior: np.ndarray, K: np.ndarray) -> float:
    """Exact I(Omega; O) in bits for a finite prior and row-stochastic kernel."""
    p = np.asarray(prior, float)
    K = np.asarray(K, float)
    q = p @ K
    joint = p[:, None] * K
    mask = joint > 0
    ratio = K[mask[:, :]] / np.broadcast_to(q, K.shape)[mask]
    return float(np.sum(joint[mask] * np.log2(ratio)))
