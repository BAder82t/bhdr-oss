# Copyright (C) 2026 Bader Alissaei / VaultBytes Innovations Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Microbenchmark for the BHDR kernel.

Pure NumPy. No CKKS dependency. Reports algorithmic quantities that are
verifiable from the kernel alone:

- rotation-key count (matches the paper's overhead table),
- plaintext BSGS wall-clock per matvec across feature dimensionalities,
- low-rank vs full-BSGS rotation-count ratio at a target relative error.

Wall-clock numbers do NOT reproduce the paper's CKKS end-to-end latency
(that requires the full pipeline, not shipped here). They only show the
algorithm's plaintext cost, which is a useful upper bound on the share
of the runtime spent in BHDR-side bookkeeping.

Run:
    python3 bench.py
"""
from __future__ import annotations

import time

import numpy as np

from bhdr_lowrank import recommend_rank, rotation_count_lowrank, svd_truncate
from bhdr_regression import (
    K_BHDR,
    R1_BHDR,
    R2_BHDR,
    bhdr_plaintext_sim,
    get_rotation_key_indices,
)


N_SLOTS = 16384
REPEATS = 5


def _pick_K_prime_split(K: int, n_slots: int) -> tuple[int, int, int]:
    """Smallest K' >= K that is a power-of-2 divisor of n_slots; balanced r1*r2."""
    K_prime = 1
    while K_prime < K:
        K_prime *= 2
    if n_slots % K_prime != 0:
        raise ValueError(f"K_prime={K_prime} does not divide n_slots={n_slots}")
    r1 = 1
    while r1 * r1 < K_prime:
        r1 *= 2
    r2 = K_prime // r1
    return K_prime, r1, r2


# (d, K) pairs from the paper's coalition-count table.
# d=5 uses exact enumeration (K = 2^d - 2). Other d use K = 2*d*ln(d)
# rounded to the antithetic-paired value reported in the paper.
CONFIGS = [
    (5,   30),
    (20,  118),
    (50,  390),
    (100, 920),
]


def _time_bhdr_matvec(d: int, K: int) -> tuple[float, float, int, int, int]:
    """Return (median_seconds, max_abs_err, K_prime, r1, r2) over REPEATS."""
    K_prime, r1, r2 = _pick_K_prime_split(K, N_SLOTS)

    rng = np.random.default_rng(seed=d * 100 + K)
    M = rng.uniform(-1.0, 1.0, size=(d, K))
    y = rng.uniform(-1.0, 1.0, size=(K,))
    phi_ref = M @ y

    M_pad = np.zeros((d, K_prime))
    M_pad[:, :K] = M
    y_pad = np.zeros(K_prime)
    y_pad[:K] = y

    timings = []
    err = 0.0
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        phi = bhdr_plaintext_sim(M_pad, y_pad, r1, r2, N_SLOTS)
        timings.append(time.perf_counter() - t0)
        err = max(err, float(np.max(np.abs(phi[:d] - phi_ref))))
    return float(np.median(timings)), err, K_prime, r1, r2


def bench_rotation_keys() -> None:
    print("== Rotation keys (paper Table: Overhead) ==")
    print(f"{'d':>4}  {'K':>5}  {'K_prime':>8}  {'r1':>3}  {'r2':>3}  {'baby':>5}  {'giant':>6}  {'repl':>5}  {'total':>6}")
    for d, K in CONFIGS:
        K_prime, r1, r2 = _pick_K_prime_split(K, N_SLOTS)
        idx = get_rotation_key_indices(K_prime, r1, r2, N_SLOTS)
        baby = sum(1 for k in idx if 1 <= k < r1)
        giant = sum(1 for k in idx if k >= r1)
        repl = sum(1 for k in idx if k < 0)
        print(f"{d:>4}  {K:>5}  {K_prime:>8}  {r1:>3}  {r2:>3}  {baby:>5}  {giant:>6}  {repl:>5}  {len(idx):>6}")
    print()


def bench_matvec_latency() -> None:
    print("== Plaintext BSGS matvec wall-clock (median of {} runs) ==".format(REPEATS))
    print(f"{'d':>4}  {'K':>5}  {'K_prime':>8}  {'time_ms':>10}  {'max_abs_err':>12}")
    for d, K in CONFIGS:
        t_sec, err, K_prime, _, _ = _time_bhdr_matvec(d, K)
        print(f"{d:>4}  {K:>5}  {K_prime:>8}  {t_sec * 1000:>10.3f}  {err:>12.2e}")
    print()


def bench_lowrank_recommendation() -> None:
    print("== Low-rank decomposition (rel-err target 1e-3) ==")
    print(f"{'d':>4}  {'K_prime':>8}  {'rec_rank':>9}  {'rel_err':>9}  {'rot_full':>9}  {'rot_lr':>7}")
    for d, K in CONFIGS:
        K_prime, _, _ = _pick_K_prime_split(K, N_SLOTS)
        rng = np.random.default_rng(seed=d)
        M = rng.uniform(-1.0, 1.0, size=(d, K))
        M_pad = np.zeros((d, K_prime))
        M_pad[:, :K] = M

        r = recommend_rank(M_pad, target_rel_err=1e-3)
        r = max(1, min(r, min(M_pad.shape)))
        factors = svd_truncate(M_pad, r)
        rot = rotation_count_lowrank(d=d, K_prime=K_prime, rank=r)
        print(
            f"{d:>4}  {K_prime:>8}  {r:>9}  "
            f"{factors.relative_error:>9.2e}  "
            f"{rot['bsgs_full']:>9}  {rot['bsgs_lowrank']:>7}"
        )
    print()


def main() -> None:
    print("BHDR microbenchmark — pure NumPy, no CKKS dependency")
    print("Paper: https://doi.org/10.5281/zenodo.19791788")
    print()
    bench_rotation_keys()
    bench_matvec_latency()
    bench_lowrank_recommendation()


if __name__ == "__main__":
    main()
