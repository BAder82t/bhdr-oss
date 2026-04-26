# Copyright (C) 2026 Bader Alissaei / VaultBytes Innovations Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Unit tests for the BHDR low-rank (M = U V) variant.

All tests are plaintext / numpy. See companion paper:
https://zenodo.org/records/19556200
"""
from __future__ import annotations

import numpy as np
import pytest

from bhdr_lowrank import (
    LowRankFactors,
    lowrank_matvec,
    recommend_rank,
    rotation_count_lowrank,
    svd_truncate,
)


def test_svd_truncate_full_rank_is_exact():
    """Truncating at full rank reconstructs M exactly."""
    rng = np.random.default_rng(0)
    M = rng.uniform(-1.0, 1.0, size=(40, 60))
    r = min(M.shape)
    factors = svd_truncate(M, r)
    M_approx = factors.U @ factors.V_T
    assert np.allclose(M_approx, M, atol=1e-10)
    assert factors.rank == r
    assert factors.frobenius_error < 1e-9


def test_svd_truncate_low_rank_input_recovers_at_target_rank():
    """Rank-r matrix is recovered exactly at rank r."""
    rng = np.random.default_rng(1)
    d, K, r = 50, 512, 8
    U_true = rng.normal(size=(d, r))
    V_true = rng.normal(size=(r, K))
    M = U_true @ V_true
    factors = svd_truncate(M, r)
    assert factors.rank == r
    assert factors.relative_error < 1e-10


def test_svd_truncate_rejects_invalid_rank():
    M = np.ones((4, 5))
    with pytest.raises(ValueError):
        svd_truncate(M, 0)
    with pytest.raises(ValueError):
        svd_truncate(M, 100)


def test_lowrank_matvec_matches_full():
    """U @ (V_T @ y) == M @ y when r is full."""
    rng = np.random.default_rng(2)
    M = rng.uniform(-1.0, 1.0, size=(30, 64))
    y = rng.uniform(-1.0, 1.0, size=(64,))
    factors = svd_truncate(M, min(M.shape))
    phi_lr = lowrank_matvec(factors, y)
    phi_ref = M @ y
    assert np.allclose(phi_lr, phi_ref, atol=1e-10)


def test_recommend_rank_returns_minimum_for_low_rank_M():
    """Rank-r matrix should be recommended at exactly rank r for tight tol."""
    rng = np.random.default_rng(3)
    d, K, r = 32, 128, 5
    U_true = rng.normal(size=(d, r))
    V_true = rng.normal(size=(r, K))
    M = U_true @ V_true
    rec = recommend_rank(M, target_rel_err=1e-8)
    assert rec == r


def test_recommend_rank_caps_at_min_dim():
    rng = np.random.default_rng(4)
    M = rng.uniform(-1.0, 1.0, size=(8, 16))
    rec = recommend_rank(M, target_rel_err=0.0)
    assert rec == min(M.shape)


def test_rotation_count_lowrank_returns_dict_with_speedup():
    out = rotation_count_lowrank(d=50, K_prime=512, rank=20)
    assert {"d", "K_prime", "rank", "bsgs_full", "bsgs_lowrank", "speedup_estimate"} <= set(out)
    assert out["d"] == 50
    assert out["K_prime"] == 512
    assert out["rank"] == 20
    assert out["bsgs_full"] > 0
    assert out["bsgs_lowrank"] > 0


def test_factors_are_immutable_dataclass():
    factors = LowRankFactors(
        U=np.zeros((2, 1)),
        V_T=np.zeros((1, 2)),
        rank=1,
        frobenius_error=0.0,
        relative_error=0.0,
    )
    with pytest.raises(Exception):
        factors.rank = 99  # frozen dataclass
