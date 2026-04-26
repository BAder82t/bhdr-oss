# BHDR — BSGS-Hoisted Diagonal Regression

Reference implementation of **BHDR**, a non-interactive single-server
construction that runs the server-side coalition evaluation and weighted
least-squares regression of Kernel SHAP under CKKS fully homomorphic
encryption.

## Paper

> Bader Alissaei. *BHDR: BSGS-Hoisted Diagonal Regression for
> Non-Interactive Single-Server Kernel SHAP under CKKS.*
> Zenodo, 2026.
> <https://zenodo.org/records/19556200>

Cite the paper for any algorithmic details, threat model, parameter
choices, and benchmark numbers.

## Contents

- `bhdr_regression.py` — full BSGS hoisted diagonal regression
  (Halevi–Shoup matvec with K-periodic replicate encoding).
- `bhdr_lowrank.py` — optional low-rank `M = U V` variant for reducing
  rotation count when `M` is near-singular.
- `bench.py` — pure-NumPy microbenchmark across `d ∈ {5, 20, 50, 100}`.
  Reports rotation-key counts, plaintext BSGS wall-clock, and low-rank
  rotation-count comparison. Does not reproduce the paper's CKKS
  end-to-end latency (that needs the full pipeline, not shipped here).
- `test_bhdr.py`, `test_bhdr_lowrank.py` — unit tests (`pytest`).

Both kernel files are pure NumPy plus a CKKS `CryptoContext` interface.
Bring your own CKKS backend (OpenFHE, etc.) that exposes
`MakeCKKSPackedPlaintext`, `EvalMult`, `EvalAdd`, and `EvalRotate`.

```
python3 -m pytest -q          # 14 unit tests
python3 bench.py              # microbenchmark
```

## License

AGPL-3.0-or-later. See `LICENSE` and `NOTICE`.

**Patent.** This repository implements a homomorphic regression kernel
covered by pending application PCT/IB2026/053405. The AGPL grant covers
source code only and does not grant any patent license. See `NOTICE`.
Inquiries: b@vaultbytes.com.
