# BHDR — BSGS-Hoisted Diagonal Regression

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19791788.svg)](https://doi.org/10.5281/zenodo.19791788)
![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)
![License: Commercial](https://img.shields.io/badge/License-Commercial-green.svg)
![Patent: PCT%2FIB2026%2F053405](https://img.shields.io/badge/Patent-PCT%2FIB2026%2F053405-orange.svg)

> **BHDR is one component of [CipherExplain](https://cipherexplain.com)** —
> the encrypted-explainability platform from VaultBytes. CipherExplain is
> the deployable product (SaaS, on-prem, OEM) that turns this kernel into
> end-to-end Kernel SHAP under CKKS, with OpenFHE production bindings,
> regulator-ready audit envelopes, and managed key handling.
>
> **For the deployable product:** [cipherexplain.com](https://cipherexplain.com)
> **This repository:** the BHDR regression kernel only — published under
> AGPL for research, reproducibility, and patent-claim disclosure.

---

Reference implementation of the **BHDR regression kernel**: a
BSGS-hoisted diagonal matrix-vector primitive for the encrypted Kernel
SHAP regression step under CKKS. This repository is a compact OSS
extraction of the regression component from the full
[CipherExplain](https://cipherexplain.com) pipeline; it does **not**
ship the full end-to-end CKKS deployment or reproduce the paper's
wall-clock numbers.

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

## Not included (ships in CipherExplain)

The following components are part of the [CipherExplain](https://cipherexplain.com)
product and are **not** in this repository:

- the full CipherExplain API service and SDK,
- OpenFHE production bindings,
- the encrypted inference pipeline (Components 100–500 of the paper),
- the offline `M = (Zᵀ W Z)⁻¹ Zᵀ W` generator,
- OCTE tree-ensemble homomorphic evaluator,
- production benchmark harnesses and CKKS end-to-end latency
  reproduction,
- regulator-ready audit envelope generation, key handling, and
  conformity-assessment artefacts.

For the deployable product see [cipherexplain.com](https://cipherexplain.com).
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

## Looking for the product, not the kernel?

Most users do not need this repository. If you want encrypted Kernel
SHAP as a deployable service — with OpenFHE bindings, audit envelopes,
key handling, and an SDK — go to **[cipherexplain.com](https://cipherexplain.com)**.

This repository exists for:

- **researchers** reproducing the BHDR microbenchmarks and citing the
  paper,
- **engineers** auditing the kernel against the patent disclosure,
- **AGPL-compatible deployments** that want the kernel only, without
  CipherExplain's product-layer features.

If you are a regulated-industry buyer (bank MRM, insurance, medtech,
government), start at [cipherexplain.com](https://cipherexplain.com) —
not here.

## License

`bhdr-oss` is published under three independent licenses to cover the
kernel-only use cases above. The deployable CipherExplain product is
licensed separately under its own commercial terms (see
[cipherexplain.com](https://cipherexplain.com)).

| License | Covers | Cost |
|---|---|---|
| [AGPL-3.0-or-later](LICENSE) | Source code copyright (default) | Free |
| [VaultBytes Commercial License](LICENSE-COMMERCIAL.md) | Kernel source, non-AGPL terms | Paid |
| [VaultBytes Patent License](LICENSE-PATENT.md) | Method claims of PCT/IB2026/053405 | Paid |

The three licenses are independent. The same Git tags ship to all
licensees. There is no closed-source build of *this kernel*, no
feature paywall in this repository, and no hidden telemetry.

**Patent notice.** This repository contains software related to
pending PCT patent application **PCT/IB2026/053405**. The AGPL license
grants no patent rights except to the minimum extent, if any,
expressly required by AGPL-3.0 itself. A standalone patent license is
required for clean-room reimplementations, ports to other FHE
libraries, hardware accelerators, and OEM embedding. CipherExplain
customers receive patent coverage as part of the product license — no
separate filing required. See [LICENSE-PATENT.md](LICENSE-PATENT.md).

**Contacts.**
Product (CipherExplain SaaS, on-prem, OEM): [cipherexplain.com](https://cipherexplain.com)
Kernel commercial / patent licensing: **b@vaultbytes.com**
