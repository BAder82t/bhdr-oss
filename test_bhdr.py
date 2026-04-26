# Copyright (C) 2026 Bader Alissaei / VaultBytes Innovations Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Unit tests for the BHDR (BSGS-Hoisted Diagonal Regression) module.

All tests are plaintext / numpy; none require a CKKS backend. The FHE
correctness was validated end-to-end against this plaintext oracle
(Pearson r = 1.00000, max_abs_err 7.9e-12). See the companion paper:
https://doi.org/10.5281/zenodo.19791788
"""
from __future__ import annotations

import numpy as np

from bhdr_regression import (
    K_BHDR,
    N_ROTATION_KEYS,
    R1_BHDR,
    R2_BHDR,
    bhdr_plaintext_sim,
    get_rotation_key_indices,
)


N_SLOTS = 16384


def test_K_prime_divides_n():
    """K' must divide N_SLOTS so the diagonal tile is aligned."""
    assert N_SLOTS % K_BHDR == 0, (
        f"K_BHDR={K_BHDR} must divide N_SLOTS={N_SLOTS}; "
        f"otherwise the mod-n wrap corrupts the diagonal tile"
    )


def test_rotation_key_count():
    """Exactly 51 unique BHDR rotation offsets."""
    indices = get_rotation_key_indices(K_BHDR, R1_BHDR, R2_BHDR, N_SLOTS)
    assert len(set(indices)) == N_ROTATION_KEYS, (
        f"expected {N_ROTATION_KEYS} unique offsets, got {len(set(indices))}"
    )
    assert len(indices) == N_ROTATION_KEYS, (
        "duplicates in rotation key list"
    )


def test_bsgs_split_covers_K():
    """r1 * r2 must equal K' exactly (no wasted multiplies, no undersized tile)."""
    assert R1_BHDR * R2_BHDR == K_BHDR
    assert R1_BHDR == 32
    assert R2_BHDR == 16
    assert K_BHDR == 512


def test_plaintext_bsgs_correctness():
    """Contiguous BSGS reproduces M @ y to floating-point precision."""
    d, K = 50, 390
    rng = np.random.default_rng(42)
    M = rng.uniform(-1.0, 1.0, size=(d, K))
    y = rng.uniform(-1.0, 1.0, size=(K,))
    phi_ref = M @ y

    M_pad = np.zeros((d, K_BHDR))
    M_pad[:, :K] = M
    y_pad = np.zeros(K_BHDR)
    y_pad[:K] = y

    phi_full = bhdr_plaintext_sim(M_pad, y_pad, R1_BHDR, R2_BHDR, N_SLOTS)
    err = float(np.max(np.abs(phi_full[:d] - phi_ref)))
    assert err < 1e-10, f"BHDR plaintext error too large: {err:.3e}"


def test_zero_padding_robustness():
    """BSGS identity is robust to zero-padding from K to K'."""
    d, K = 50, 390
    rng = np.random.default_rng(7)
    M = rng.uniform(-1.0, 1.0, size=(d, K))
    y = rng.uniform(-1.0, 1.0, size=(K,))
    phi_ref = M @ y

    M_pad = np.zeros((d, K_BHDR))
    M_pad[:, :K] = M
    y_pad = np.zeros(K_BHDR)
    y_pad[:K] = y

    phi_full = bhdr_plaintext_sim(M_pad, y_pad, R1_BHDR, R2_BHDR, N_SLOTS)
    err = float(np.max(np.abs(phi_full[:d] - phi_ref)))
    assert err < 1e-10, f"zero-pad BHDR error too large: {err:.3e}"


def test_rotation_key_structure():
    """Rotation keys partition cleanly into baby / giant / replication."""
    idx = get_rotation_key_indices(K_BHDR, R1_BHDR, R2_BHDR, N_SLOTS)
    baby = sorted(k for k in idx if 1 <= k < R1_BHDR)
    giant = sorted(k for k in idx if k >= R1_BHDR)
    repl = sorted(k for k in idx if k < 0)

    assert baby == list(range(1, R1_BHDR))                          # 1..31
    assert giant == [j * R1_BHDR for j in range(1, R2_BHDR)]        # 32..480
    assert repl == [-s for s in (8192, 4096, 2048, 1024, 512)]      # 5 repl
    assert len(baby) + len(giant) + len(repl) == N_ROTATION_KEYS
