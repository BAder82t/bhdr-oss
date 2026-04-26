# Copyright (C) 2026 Bader Alissaei / VaultBytes Innovations Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later
# Patent pending: PCT/IB2026/053405
# See NOTICE and LICENSE files for details.

"""BSGS-Hoisted Diagonal Regression (BHDR).

Replaces the row-by-row WLS dot-product regression with a Halevi-Shoup diagonal
matmul accelerated by baby-step/giant-step (BSGS) decomposition. See the
companion paper (https://zenodo.org/records/19556200) for the full
construction, threat model, and benchmark methodology.

Two algorithmic corrections vs a naive Halevi-Shoup spec, discovered during
validation:

1. **K-periodic replicate encoding.** The doc's description (zero-pad M in
   n x n, BSGS over k=0..K-1) produces the correct sum only at slot 0.
   phi[l] for l >= 1 needs the wrap-around diagonals at k in [n-l, n-1],
   which are not covered by a {0..K-1} rotation set. The Halevi-Shoup fix
   is to tile y (and each diagonal) with period K across the n slots,
   making the BSGS identity hold at every output slot l < d. The tiling
   step on Enc(y) requires ceil(log2(n/K)) rotate+add doublings.

2. **K must divide n.** K=390 does not divide n=16384; the mod-n wrap in
   the plaintext roll corrupts the tile by (n mod K)=4 slots whenever a
   giant-step shift j*r1 exceeds the output slot index. Round K up to
   K'=512 (next power-of-2 divisor of 16384). Pad M with (K' - K) zero
   columns; those slots contribute zero to the accumulator.

Runtime cost (measured, 4 vCPU AMD EPYC-Genoa):
    std-basis path (Python/OpenFHE bindings): ~11s regression step
    ext-basis path (C++): ~5.3s regression step
Python bindings do not currently expose EvalMultExt / EvalFastRotationExt;
the std-basis path is the portable reference implementation.

Rotation keys needed: 51 total
    Baby-step    : {1, 2, ..., r1 - 1} = {1..31}     (31 keys)
    Giant-step   : {r1, 2*r1, ..., (r2 - 1)*r1} = {32, 64, ..., 480}  (15 keys)
    Replication  : {-K', -2K', -4K', ..., -n/2}    (5 keys)

Depth consumed: +1 (one Rescale).
"""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np

# Canonical constants — single source of truth for the BHDR parameters.
# K_BHDR must divide your CKKS N_SLOTS (default 16384; 16384 / 512 = 32).
K_BHDR = 512          # BSGS cycle length
R1_BHDR = 32          # baby-step count; asymm-optimized split with R2_BHDR
R2_BHDR = 16          # giant-step count
N_ROTATION_KEYS = 51  # 31 baby + 15 giant + 5 replication

# Sanity: BSGS tiling must be exact.
assert R1_BHDR * R2_BHDR == K_BHDR, "r1 * r2 must equal K'"


# --------------------------------------------------------------------------
# Plaintext helpers (offline preprocessing + test simulation)
# --------------------------------------------------------------------------


def _tile_period(v_K: np.ndarray, n: int) -> np.ndarray:
    """Tile v_K across n slots with exact period. Requires len(v_K) | n."""
    K = v_K.size
    if n % K != 0:
        raise ValueError(
            f"K-periodic tile requires K ({K}) to divide n ({n}); "
            f"use K' that divides n instead of K"
        )
    return np.tile(v_K, n // K)


def _roll(v: np.ndarray, s: int) -> np.ndarray:
    """np.roll-equivalent helper: out[l] = v[(l - s) mod n]."""
    return np.roll(v, s)


def _build_diagonal_grid_numpy(
    M: np.ndarray, d: int, K_prime: int, r1: int, r2: int, n_slots: int
) -> list[list[np.ndarray]]:
    """Return the r2 x r1 grid of tiled+shifted diagonals as numpy arrays."""
    M_tilde = np.zeros((K_prime, K_prime), dtype=np.float64)
    M_tilde[:d, :] = M  # M already padded to shape (d, K_prime)

    grid: list[list[np.ndarray]] = [[None] * r1 for _ in range(r2)]  # type: ignore[list-item]
    for k in range(r1 * r2):
        dk_K = np.array(
            [M_tilde[l, (l + k) % K_prime] for l in range(K_prime)],
            dtype=np.float64,
        )
        dk_n = _tile_period(dk_K, n_slots)
        j, i = divmod(k, r1)
        grid[j][i] = _roll(dk_n, j * r1)
    return grid


def bhdr_plaintext_sim(
    M_pad: np.ndarray,
    y_pad: np.ndarray,
    r1: int = R1_BHDR,
    r2: int = R2_BHDR,
    n_slots: int = 16384,
) -> np.ndarray:
    """Pure-numpy BHDR simulator. Returns the n-slot result; phi[i] at slot i.

    Arguments:
        M_pad: (d, K') zero-padded regression matrix.
        y_pad: length K' zero-padded coalition outputs.
        r1, r2: BSGS split (r1 * r2 == K').
        n_slots: CKKS slot count.
    """
    d, K_prime = M_pad.shape
    if r1 * r2 != K_prime:
        raise ValueError(f"r1*r2 ({r1 * r2}) must equal K' ({K_prime})")

    # Replicate y with period K' across the n slots.
    y_replicated = _tile_period(y_pad, n_slots)

    # Diagonal grid (plaintext).
    grid = _build_diagonal_grid_numpy(M_pad, d, K_prime, r1, r2, n_slots)

    # Baby-step rotated copies of y_replicated.
    baby = [np.roll(y_replicated, -i) for i in range(r1)]  # left rotate by i

    phi_n = np.zeros(n_slots, dtype=np.float64)
    for j in range(r2):
        acc_j = np.zeros(n_slots, dtype=np.float64)
        for i in range(r1):
            acc_j += grid[j][i] * baby[i]
        phi_n += np.roll(acc_j, -(j * r1))  # left rotate by j*r1
    return phi_n


# --------------------------------------------------------------------------
# FHE helpers (run at key-gen / encryption time)
# --------------------------------------------------------------------------


def get_rotation_key_indices(
    K_prime: int = K_BHDR,
    r1: int = R1_BHDR,
    r2: int = R2_BHDR,
    n_slots: int = 16384,
) -> list[int]:
    """Return the 51 BHDR-specific rotation offsets.

    Baby-step offsets rotate the replicated Enc(y) within the K'-periodic
    tile. Giant-step offsets rotate the per-giant-step accumulators
    together. Replication offsets fill the K'-periodic tile at encryption
    time; they are RIGHT-rotations (negative indices in OpenFHE's
    left-positive convention), because each replication doubling moves
    data from low slots to higher slots.
    """
    baby = list(range(1, r1))                       # 1..r1-1
    giant = [j * r1 for j in range(1, r2)]          # r1..(r2-1)*r1

    repl: list[int] = []
    stride = K_prime
    while stride < n_slots:
        repl.append(-stride)                        # right-rotation
        stride *= 2

    return baby + giant + repl


def precompute_bhdr_grid(
    M: np.ndarray,
    d: int,
    K_prime: int,
    r1: int,
    r2: int,
    n_slots: int,
    cc: Any,
) -> list[list[Any]]:
    """Precompute the r2 x r1 grid of standard-basis CKKS plaintexts.

    Arguments:
        M: (d, K) original WLS regression matrix (K may be < K_prime).
        d: feature count.
        K_prime: BSGS cycle; must divide n_slots.
        r1, r2: BSGS split, r1 * r2 == K_prime.
        n_slots: CKKS slot count.
        cc: OpenFHE CryptoContext for `MakeCKKSPackedPlaintext`.
    """
    if n_slots % K_prime != 0:
        raise ValueError(
            f"K_prime ({K_prime}) must divide n_slots ({n_slots})"
        )
    if r1 * r2 != K_prime:
        raise ValueError(f"r1*r2 ({r1 * r2}) must equal K_prime ({K_prime})")

    K_orig = M.shape[1]
    M_pad = np.zeros((d, K_prime), dtype=np.float64)
    M_pad[:, :K_orig] = M

    # --- FIX (2026-04-24): diagnose potential CKKS overflow at grid build ---
    # The worst-case accumulator magnitude is |M|_inf * K_prime * |y|_inf.
    # If it crosses the scale factor, downstream EvalMult silently wraps.
    import logging as _logging
    _log = _logging.getLogger(__name__)
    m_inf = float(np.abs(M_pad).max())
    # Heuristic: coalition outputs for sigmoid lie in [0, 1] and are centred
    # to [-0.5, 0.5] before regression. Adjust if your pipeline differs.
    y_bound_assumed = 0.5
    worst_case = m_inf * K_prime * y_bound_assumed
    # CKKS scale default in this repo is 2**50; use the log2 budget check.
    import math as _math
    bits = _math.log2(worst_case + 1e-300)
    if bits > 48.0:
        _log.warning(
            "BHDR worst-case accumulator %.2f bits > 48-bit safety budget "
            "(|M|_inf=%.3g, K'=%d, y_bound=%.3g); consider rescaling M",
            bits, m_inf, K_prime, y_bound_assumed,
        )

    grid_np = _build_diagonal_grid_numpy(M_pad, d, K_prime, r1, r2, n_slots)
    grid: list[list[Any]] = [[None] * r1 for _ in range(r2)]
    for j in range(r2):
        for i in range(r1):
            grid[j][i] = cc.MakeCKKSPackedPlaintext(grid_np[j][i].tolist())
    return grid


def gather_coalition_outputs(
    ct_eval_list: Sequence[Any],
    d: int,
    K: int,
    K_prime: int,
    n_slots: int,
    cc: Any,
) -> Any:
    """Consolidate 2 stride-d packed ciphertexts into a single Enc(y).

    The upstream coalition-evaluation step packs K coalitions into
    ceil(K / floor(n_slots / d)) ciphertexts, with coalition c occupying
    slots [c*d, (c+1)*d). The regression only needs the first slot of each
    block (the mean coalition output y_c). This function:

      1. Masks each input ct to zero everything except slot c*d.
      2. Rotates the second batch so its y values fall at slot positions
         past the first batch's range, producing a single packed Enc(y)
         with y_k at slot k*d for k in [0, K).

    Slots [K*d, n_slots) in the output are zero — which is exactly what
    the zero-padded M_pad's K_prime-K "fake" columns expect.

    Cost: 2 pt-ct mult + 1 rotation + 1 addition. Depth: 0.
    """
    if len(ct_eval_list) != 2:
        raise ValueError(
            f"gather expects exactly 2 input ciphertexts, got "
            f"{len(ct_eval_list)}"
        )
    # Current Component 300 packs with stride d: coalition c at slot c*d.
    # First batch: coalitions [0, batch1_size). Second: [batch1_size, K).
    batch1_size = n_slots // d                 # floor(n_slots / d)
    if batch1_size >= K:
        batch1_size = K                        # single-batch case
    batch2_size = K - batch1_size

    mask1 = np.zeros(n_slots, dtype=np.float64)
    for c in range(batch1_size):
        mask1[c * d] = 1.0
    mask2 = np.zeros(n_slots, dtype=np.float64)
    for c in range(batch2_size):
        mask2[c * d] = 1.0

    pt_mask1 = cc.MakeCKKSPackedPlaintext(mask1.tolist())
    pt_mask2 = cc.MakeCKKSPackedPlaintext(mask2.tolist())

    m1 = cc.EvalMult(ct_eval_list[0], pt_mask1)
    m2 = cc.EvalMult(ct_eval_list[1], pt_mask2)

    offset = batch1_size * d
    if offset > 0:
        # Shift batch 2's y values from slots [0, batch2*d) to
        # [batch1*d, batch1*d + batch2*d). OpenFHE's EvalRotate uses
        # positive = left rotation, so a right rotation by `offset` is
        # expressed as -offset.
        m2 = cc.EvalRotate(m2, -offset)
    return cc.EvalAdd(m1, m2)


def _replicate_period_K(ct: Any, K_prime: int, n_slots: int, cc: Any) -> Any:
    """Replicate y (at slots 0..K'-1, zero elsewhere) with period K'.

    Uses log2(n_slots / K') rotate-and-add doublings. Requires rotation
    keys at offsets {-K', -2K', ..., -n_slots / 2}. See
    get_rotation_key_indices for the exact key set.
    """
    if n_slots % K_prime != 0:
        raise ValueError(
            f"K_prime ({K_prime}) must divide n_slots ({n_slots})"
        )
    result = ct
    stride = K_prime
    while stride < n_slots:
        rotated = cc.EvalRotate(result, -stride)
        result = cc.EvalAdd(result, rotated)
        stride *= 2
    return result


def bhdr(
    enc_y: Any,
    grid: list[list[Any]],
    r1: int,
    r2: int,
    K_prime: int,
    n_slots: int,
    cc: Any,
) -> Any:
    """Run the full BHDR regression in standard basis.

    Arguments:
        enc_y: CKKS ciphertext holding y contiguous at slots [0, K).
        grid: r2 x r1 precomputed plaintexts from precompute_bhdr_grid.
        r1, r2: BSGS split.
        K_prime: BSGS cycle length.
        n_slots: CKKS slot count.
        cc: OpenFHE CryptoContext.

    Returns: Enc(phi_hat) with phi[0..d-1] at slots 0..d-1 (repeated every
    K' slots, which is irrelevant: only the first d slots are read).
    Depth consumed: +1 (one Rescale).
    """
    # Phase 1: replicate y with period K' across all n_slots slots.
    ct_y_rep = _replicate_period_K(enc_y, K_prime, n_slots, cc)

    # Phase 2: baby-step rotations (standard basis).
    ct_baby = [ct_y_rep]
    for i in range(1, r1):
        ct_baby.append(cc.EvalRotate(ct_y_rep, i))

    # Phase 3: giant-step accumulation.
    result = None
    for j in range(r2):
        acc_j = cc.EvalMult(ct_baby[0], grid[j][0])
        for i in range(1, r1):
            acc_j = cc.EvalAdd(acc_j, cc.EvalMult(ct_baby[i], grid[j][i]))
        if j == 0:
            result = acc_j
        else:
            result = cc.EvalAdd(result, cc.EvalRotate(acc_j, j * r1))

    # Phase 4: depth cleanup. EvalMult already performed rescaling in
    # OpenFHE's default chain; no explicit Rescale needed in the std-basis
    # path because EvalMult auto-rescales by one level. The remaining
    # level budget is unchanged vs the legacy path (both consume +1).
    return result
