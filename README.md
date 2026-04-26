# BHDR — BSGS-Hoisted Diagonal Regression

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19791788.svg)](https://doi.org/10.5281/zenodo.19791788)
![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)

Reference implementation of the **BHDR regression kernel**: a
BSGS-hoisted diagonal matrix-vector primitive for the encrypted Kernel
SHAP regression step under CKKS. This repository is a compact OSS
extraction of the regression component from the full CipherExplain /
BHDR pipeline; it does **not** ship the full end-to-end CKKS deployment
or reproduce the paper's wall-clock numbers.

## Paper

> Bader Alissaei. *BHDR: BSGS-Hoisted Diagonal Regression for
> Non-Interactive Single-Server Kernel SHAP under CKKS.*
> Zenodo, 2026. doi: [10.5281/zenodo.19791788](https://doi.org/10.5281/zenodo.19791788).

```bibtex
@misc{alissaei2026bhdr,
  author    = {Bader Alissaei},
  title     = {{BHDR}: {BSGS}-Hoisted Diagonal Regression for
               Non-Interactive Single-Server Kernel {SHAP} under {CKKS}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19791788},
  url       = {https://doi.org/10.5281/zenodo.19791788}
}
```

## Included

- `bhdr_regression.py` — BSGS hoisted diagonal regression
  (Halevi–Shoup matvec with K-periodic replicate encoding).
- `bhdr_lowrank.py` — experimental low-rank `M = U V` variant.
- `bench.py` — pure-NumPy microbenchmark across `d ∈ {5, 20, 50, 100}`.
- `test_bhdr.py`, `test_bhdr_lowrank.py` — unit tests.

Both kernel files are pure NumPy plus a CKKS `CryptoContext` interface.
Bring your own CKKS backend (OpenFHE, etc.) that exposes
`MakeCKKSPackedPlaintext`, `EvalMult`, `EvalAdd`, and `EvalRotate`.

## Not included

- the full CipherExplain API service,
- OpenFHE production bindings,
- the encrypted inference pipeline (Components 100–500 of the paper),
- the offline `M = (Zᵀ W Z)⁻¹ Zᵀ W` generator,
- OCTE tree-ensemble homomorphic evaluator,
- production benchmark harnesses and CKKS end-to-end latency reproduction.

For the full system design and deployed benchmarks, cite the
[technical report](https://doi.org/10.5281/zenodo.19791788).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q          # 14 unit tests
python3 bench.py   # microbenchmark
```

## Minimal example

```python
import numpy as np
from bhdr_regression import K_BHDR, R1_BHDR, R2_BHDR, bhdr_plaintext_sim

d, K, n_slots = 50, 390, 16384
M = np.random.default_rng(0).uniform(-1.0, 1.0, size=(d, K))
y = np.random.default_rng(1).uniform(-1.0, 1.0, size=(K,))

M_pad = np.zeros((d, K_BHDR)); M_pad[:, :K] = M
y_pad = np.zeros(K_BHDR);      y_pad[:K] = y

phi = bhdr_plaintext_sim(M_pad, y_pad, R1_BHDR, R2_BHDR, n_slots)
print(np.allclose(phi[:d], M @ y))   # True (to FP precision)
```

## License

AGPL-3.0-or-later. See `LICENSE` and `NOTICE`.

**Patent notice.** This repository contains software related to pending
PCT patent application PCT/IB2026/053405. The software is licensed
under AGPL-3.0-or-later. No patent rights are granted except to the
extent, if any, expressly required by the applicable software license.
Commercial, proprietary, or non-AGPL licensing inquiries:
b@vaultbytes.com.
