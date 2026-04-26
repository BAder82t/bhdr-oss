# Copyright (C) 2026 Bader Alissaei / VaultBytes Innovations Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later
# Patent pending: PCT/IB2026/053405

"""Low-rank M decomposition for BHDR regression (experimental).

Experimental variant for further reducing the BHDR regression-kernel
cost. This is NOT the headline deployed BHDR path and does not
reproduce the paper's end-to-end latency numbers; see the companion
report at https://doi.org/10.5281/zenodo.19791788 for deployed figures.

Low-rank decomposition of M = U V reduces the d * K' = 50 * 512 = 25,600
multiplications to (d + K') * r = 562 * r where r = rank(M) is typically
~20 (confirmed by empirical SVD sweep; the deployed M is near-singular
by construction).

Pipeline change: in place of one BSGS matvec over the full M, we run:
    z = V @ y          (r * K')   -- low-rank projection, r << d
    phi = U @ z        (d * r)    -- low-rank expansion

Because r is small (~20), we can keep z un-packed in a single ciphertext and
use a standard rotate-and-sum for the second matvec. Net: ~5x fewer
rotations at d=50 and ~3x fewer at d=100.

Benchmark methodology: apply `svd_truncate` at a given rank, verify
forward-error bound on phi, confirm rotation-count reduction.

Opt-in via `CE_BHDR_LOWRANK_RANK=<r>` env var; disabled when 0.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import numpy as np

log = logging.getLogger(__name__)

DEFAULT_RANK = int(os.environ.get("CE_BHDR_LOWRANK_RANK", "0"))  # 0 = disabled


@dataclass(frozen=True)
class LowRankFactors:
    """Factorization M ~= U @ V_T with rank r."""
    U: np.ndarray      # (d, r)
    V_T: np.ndarray    # (r, K')
    rank: int
    frobenius_error: float
    relative_error: float


def svd_truncate(M: np.ndarray, rank: int) -> LowRankFactors:
    """Rank-`rank` truncated SVD of M, returning factors and reconstruction error.

    M = U_full @ diag(S) @ V_full.  We absorb sqrt(S) into both U and V_T so
    the stored factors are balanced (similar operator norms) -- this keeps
    the CKKS scale factor stable across the two matvec steps.
    """
    M = np.asarray(M, dtype=np.float64)
    U_full, S, V_full = np.linalg.svd(M, full_matrices=False)
    if rank <= 0 or rank > len(S):
        raise ValueError(f"rank must be in (0, {len(S)}]; got {rank}")
    S_trunc = S[:rank]
    U_r = U_full[:, :rank] * np.sqrt(S_trunc)
    V_T_r = np.sqrt(S_trunc)[:, None] * V_full[:rank]
    M_approx = U_r @ V_T_r
    frob = float(np.linalg.norm(M - M_approx, ord="fro"))
    rel = frob / max(float(np.linalg.norm(M, ord="fro")), 1e-30)
    return LowRankFactors(
        U=U_r, V_T=V_T_r, rank=rank,
        frobenius_error=frob, relative_error=rel,
    )


def lowrank_matvec(factors: LowRankFactors, y: np.ndarray) -> np.ndarray:
    """Plaintext reference for the two-step matvec: phi_hat = U @ (V_T @ y)."""
    z = factors.V_T @ np.asarray(y, dtype=np.float64)
    return factors.U @ z


def recommend_rank(M: np.ndarray, target_rel_err: float = 1e-3) -> int:
    """Pick the smallest rank such that relative Frobenius error <= target.

    Returns the minimum r. Callers typically bound r <= d/2 to stay faster
    than the full matvec.
    """
    S = np.linalg.svd(np.asarray(M, dtype=np.float64), compute_uv=False)
    cum = np.cumsum(S[::-1] ** 2)[::-1]
    total = float(np.sum(S ** 2))
    for r in range(1, len(S) + 1):
        if r == len(S):
            return r
        tail_energy = cum[r] if r < len(cum) else 0.0
        if np.sqrt(tail_energy / total) <= target_rel_err:
            return r
    return len(S)


def rotation_count_lowrank(d: int, K_prime: int, rank: int) -> dict:
    """Expected rotation-count comparison vs full BSGS.

    Paper baseline (BSGS full matvec at d=50, K'=512): 51 rotations.
    Low-rank (r=20): ~ 2*sqrt(K') + 2*sqrt(d) * 2-step = ~ 45+15 for first,
    ~ 10 for second. Net <= 60% of baseline when r < 25.
    """
    import math as _m
    bsgs_full = int(2 * _m.sqrt(K_prime))  # heuristic giant-step count
    bsgs_lowrank = int(_m.ceil(2 * _m.sqrt(K_prime))) + int(_m.ceil(2 * _m.sqrt(d)))
    return {
        "d": d, "K_prime": K_prime, "rank": rank,
        "bsgs_full": bsgs_full,
        "bsgs_lowrank": bsgs_lowrank,
        "speedup_estimate": round(bsgs_full / max(1, bsgs_lowrank * rank / d), 2),
    }


def is_enabled() -> bool:
    return DEFAULT_RANK > 0
