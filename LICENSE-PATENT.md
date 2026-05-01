# Patent License

> **CipherExplain customers do not need a separate patent license.**
> The product license at [cipherexplain.com](https://cipherexplain.com)
> already covers PCT/IB2026/053405 for the licensed deployment. This
> page applies only to parties who are not CipherExplain customers
> and who implement the patented method in their own code (clean-room
> reimplementations, ports to other FHE libraries, hardware
> accelerators, OEM platforms).

`bhdr-oss` is offered under three independent licenses:

1. **AGPL-3.0-or-later** — covers source code copyright. See
   [LICENSE](LICENSE) and [LICENSING.md](LICENSING.md).
2. **VaultBytes Commercial License** — paid, non-AGPL terms for the
   same source code. See [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md).
3. **VaultBytes Patent License** — paid license to the method claims
   of PCT/IB2026/053405, independent of which source code (this
   repository or an independent reimplementation) embodies them. This
   page describes that license.

Patent rights and copyright are independent. The AGPL license on this
repository does **not** grant patent rights except to the minimum
extent, if any, expressly required by AGPL-3.0 §11 itself. The
VaultBytes Commercial License grants a covenant-not-to-sue scoped to
the licensed `bhdr-oss` deployment but does not, by itself, grant
freedom to assert the method in a clean-room reimplementation, a port
to a different FHE library, or a hardware accelerator. For those
cases, a standalone patent license is required.

---

## Patent in scope

**PCT/IB2026/053405 — System and Method for Computing Shapley Additive
Explanations under Fully Homomorphic Encryption Using Compressed
Coalition Sampling.**

Patent status: PENDING (PCT national-phase entry pending).

The pending claims read on, among other things:

- non-interactive single-server Kernel SHAP under CKKS,
- compressed coalition sampling that admits a `K`-periodic replicate
  encoding,
- BSGS-hoisted diagonal matrix-vector evaluation of the regression
  step,
- low-rank `M = U V` decomposition of the Kernel SHAP regression
  operator under CKKS depth budgets,
- and the offline `M = (Zᵀ W Z)⁻¹ Zᵀ W` generator pipeline that
  produces the deployed regression operator.

Final scope is set by the granted claims of each national-phase
application. Until grant, the patent license is forward-looking and
attaches automatically to the granted claims when issued in each
designated jurisdiction.

---

## Who needs a patent license

You need a patent license if **any** of the following apply:

- You implement the patented method in code you wrote yourself (a
  clean-room reimplementation, a port to a different FHE library such
  as SEAL, HEAAN, or Lattigo, a GPU port, or a hardware accelerator)
  and you intend to use that implementation commercially.
- You build a product, platform, or service that performs encrypted
  Kernel SHAP using compressed coalition sampling and BSGS-hoisted
  diagonal regression, regardless of which source code you started
  from.
- You are an FHE library vendor, MLOps platform, or model-risk vendor
  who wants to ship the patented primitive as part of your product
  under your own branding.
- You are a regulated-industry deployer (banking, insurance,
  medical-device, government) whose procurement function requires
  standalone patent assurance separable from the source code license.

You do **not** need a patent license to:

- Cite the paper or reproduce its results in academic publications.
- Run the unit tests, microbenchmarks, or evaluation in a sandbox
  under AGPL-3.0.
- Operate an internal AGPL-compatible deployment of unmodified
  `bhdr-oss` strictly for non-commercial research, provided your use
  does not extend the patented method beyond what AGPL-3.0 §11
  requires.

If your situation is unclear, contact **b@vaultbytes.com** before you
deploy. A short written confirmation is free.

---

## What the patent license grants

A patent license is a written agreement between VaultBytes
Innovations Ltd and the licensee. Standard terms include:

- A non-exclusive, worldwide, non-transferable license under
  PCT/IB2026/053405 (and any granted national-phase counterpart) to
  practice the licensed claims, scoped to the licensed field of use
  and the licensed deployment volume.
- Optional **field-of-use grants** so a licensee in one industry
  (e.g. retail credit scoring) does not pay for fields it does not
  operate in (e.g. medical-device explainability).
- Optional **per-jurisdiction grants** for licensees who operate only
  in specific PCT national-phase territories.
- A covenant-not-to-sue for VaultBytes patents reading on the licensed
  field of use, regardless of which source code embodies the method,
  for the term of the license.
- An **option to upgrade** to a combined source + patent license under
  [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) if the licensee later
  decides to ship `bhdr-oss` itself rather than a reimplementation.

The exact scope, royalty model, term, audit rights, and termination
triggers live in the signed master patent license agreement. This page
is informational; nothing on it constitutes a binding offer.

---

## Royalty models (indicative)

Royalty model is selected per-licensee based on deployment shape.
Pricing is confirmed in writing per quote.

| Model | Target licensee | Structure |
|---|---|---|
| Flat annual | Single-jurisdiction enterprise deployment | Fixed annual fee per field of use |
| Per-deployment | Multi-tenant SaaS or platform vendor | Annual fee per deployed environment, with volume tiers |
| Per-instance royalty | OEM embedders shipping the method to end customers | Royalty per shipped instance or per active customer |
| Revenue share | Vendors whose product is built around the method | Percentage of attributable product revenue, with floor |
| Patent-only standalone | Licensees using a clean-room reimplementation | Flat annual + per-jurisdiction multipliers |

Field-of-use and per-jurisdiction multipliers apply on top of the
selected model. Combined source + patent licenses receive a discount
relative to taking the two licenses separately.

---

## How to obtain a patent license

Email **b@vaultbytes.com** with:

- Legal entity name, registered address, and country of incorporation.
- A one-paragraph description of the implementation: which FHE
  library or hardware target, which fields of use you intend to
  operate in, which PCT national-phase jurisdictions you require, and
  approximate deployment volume.
- Whether your implementation is a port of `bhdr-oss`, a clean-room
  reimplementation from the paper, or a hybrid.
- Whether you also need a source code license under
  [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md), or whether the
  patent license alone is sufficient.
- Procurement contact and preferred contracting vehicle (direct,
  reseller, or marketplace).

Standard turnaround for a quote is five business days; patent quotes
take longer than source-code quotes because field-of-use and
jurisdiction scoping requires individual review. An evaluation patent
license — free, time-limited, no production assertion — is available
on request for active proof-of-concept work.

---

## What this license does not do

- It does not grant any rights to VaultBytes trademarks beyond
  reasonable nominative use ("implementation of the BHDR method").
- It does not warrant that the patent will be granted in any specific
  jurisdiction. Royalty obligations attach only to claims that issue.
- It does not constitute legal advice on whether your specific
  implementation reads on the claims. If you require a freedom-to-
  operate opinion, retain independent counsel.
- It does not cover patents owned by third parties whose claims your
  implementation may also read on. The licensee is responsible for
  third-party freedom-to-operate.

---

Product (CipherExplain — patent rights bundled): [cipherexplain.com](https://cipherexplain.com)
Standalone patent licensing contact: **b@vaultbytes.com**
