# Commercial License

> **Looking for the CipherExplain product?** Most commercial users
> want [cipherexplain.com](https://cipherexplain.com), not a kernel
> license. CipherExplain is the deployable encrypted-SHAP platform
> that wraps BHDR with OpenFHE bindings, audit envelopes, key
> handling, and an SDK; its commercial terms are negotiated under its
> own product license, not under this page. The license below applies
> only when a customer explicitly wants the BHDR *kernel source* under
> non-AGPL terms (e.g. to embed it into their own platform without
> using CipherExplain).

`bhdr-oss` is offered under three independent licenses:

1. **AGPL-3.0-or-later** — the default. See [LICENSE](LICENSE) and
   [LICENSING.md](LICENSING.md).
2. **VaultBytes Commercial License** — a paid alternative that grants
   the same source code under non-AGPL terms. This page describes that
   license.
3. **VaultBytes Patent License** — a separate paid license to the
   method claims of PCT/IB2026/053405. See
   [LICENSE-PATENT.md](LICENSE-PATENT.md).

The commercial license and the AGPL license cover the same source
code. There is no closed-source build, no feature paywall, and no
telemetry only present in the commercial build. Commercial licensees
receive the same Git tags as AGPL users, plus the rights, indemnity,
and support enumerated below.

---

## Who needs a commercial license

You need a commercial license if **any** of the following apply:

- You ship `bhdr-oss` (modified or unmodified) inside a product or
  service whose source you do not want to release under AGPL-3.0.
- You operate a hosted service (SaaS, internal portal, regulator
  console, model-risk platform, encrypted-explainability API) that
  exposes BHDR primitives over a network and you do not want AGPL
  §13's source-disclosure obligation to extend to that service.
- You link `bhdr-oss` into a proprietary library or proprietary
  pipeline whose other components are not AGPL-compatible.
- Your legal, procurement, or compliance function has a categorical
  prohibition on AGPL-licensed dependencies (common in regulated
  banking, insurance, medical-device, and government supply chains).
- You require contractual indemnity for IP infringement claims or
  service-level commitments for security patches, neither of which
  AGPL-3.0 provides.

You do **not** need a commercial license to:

- Read, study, fork, or modify the source under AGPL-3.0.
- Run the kernel and tests inside an organisation whose other internal
  software you are willing to release under AGPL-3.0.
- Cite the paper, reproduce the microbenchmarks, or run the unit tests
  in a sandbox.
- Distribute an AGPL-3.0 fork of `bhdr-oss` provided you respect the
  AGPL terms and the trademark notice in [LICENSING.md](LICENSING.md).

If you are unsure whether your deployment requires a commercial
license, contact us before you deploy. A short written confirmation is
free and faster than a retrospective compliance review.

---

## What the commercial license grants

A commercial license is a written agreement between VaultBytes
Innovations Ltd and the licensee. Standard terms include:

- A non-exclusive, worldwide, non-transferable right to use, modify,
  and distribute `bhdr-oss` outside the AGPL-3.0 obligations, scoped
  to the licensed deployment.
- Permission to embed `bhdr-oss` in proprietary products and to
  operate proprietary network services that depend on it without
  triggering AGPL §13.
- A covenant-not-to-sue scoped to the licensed deployment for any
  VaultBytes patents (including PCT/IB2026/053405) reading on the
  licensed `bhdr-oss` releases. Standalone patent licenses for
  non-`bhdr-oss` use (clean-room reimplementations, ports to other
  FHE libraries, hardware accelerators) are negotiated separately
  under [LICENSE-PATENT.md](LICENSE-PATENT.md).
- Capped indemnity for third-party intellectual-property infringement
  claims arising from unmodified `bhdr-oss` releases.
- A defined support level: response times for security advisories,
  named-channel access for integration questions, and pre-disclosure
  of CVEs affecting the licensed releases.
- Optional add-ons: OpenFHE production-binding integration, custom
  matrix-shape tuning (BSGS dimensions, low-rank `M = U V` factor
  selection), validation harness against the licensee's SHAP pipeline,
  and on-site integration support.

The exact wording of every clause lives in the signed master license
agreement. This page is informational; nothing on it constitutes a
binding offer.

---

## What the commercial license does not change

- The numerical guarantees, BSGS shape, replicate encoding, and
  CryptoContext interface are identical across both licenses. A
  commercial licensee's BHDR output is byte-for-byte reproducible
  against an AGPL deployment given the same inputs and the same CKKS
  parameters.
- The "Not included" scope statement in [README.md](README.md)
  applies in full. A commercial license does not turn a regression
  kernel into a finished encrypted-SHAP product, deployment, or
  regulatory submission.
- The trademark policy in [LICENSING.md](LICENSING.md) applies to
  commercial licensees and AGPL forks alike.

---

## Pricing tiers (indicative)

Pricing is confirmed in writing per quote. The tiers below are
indicative, not binding.

| Tier | Target licensee | Model |
|---|---|---|
| Evaluation | POC, ≤ 90 days, no production traffic | Free, time-limited |
| Startup | Single deployment, <$5M ARR licensee | Flat annual |
| Enterprise | Bank, insurer, medical-device vendor, government | Annual per deployment, with indemnity and SLA |
| OEM | Embed BHDR in a vendor's platform | Royalty per instance or % of vendor product price |

---

## How to obtain a commercial license

Email **b@vaultbytes.com** with:

- Legal entity name, registered address, and country of incorporation.
- A one-paragraph description of the deployment: matrix dimension `d`,
  coalition count `K`, approximate envelope volume per year, internal
  vs customer-facing, and which CKKS backend you intend to use.
- Whether you require a perpetual license, a fixed-term license, or
  an evaluation license.
- Whether you also need a standalone patent license under
  [LICENSE-PATENT.md](LICENSE-PATENT.md), or whether the in-license
  covenant-not-to-sue is sufficient.
- Procurement contact and preferred contracting vehicle (direct,
  reseller, or marketplace).

Standard turnaround for a quote is two business days. An evaluation
license — free, time-limited, no production traffic — is available on
request and is the fastest way to start integration without waiting
for procurement.

---

## Frequently asked questions

**We are evaluating `bhdr-oss` and have not deployed it. Do we need a
license?**
No. Reading source, running tests in a sandbox, and reproducing the
microbenchmarks are covered by AGPL-3.0. You only need a commercial
license when you deploy in a way that triggers AGPL §13 or links into
proprietary code.

**Can we contribute back patches?**
External contributions are not accepted; this keeps the copyright
clean and makes dual-licensing possible. Customers with custom-shape
or custom-backend requirements should raise them via the commercial
channel.

**Does the commercial license cover patents?**
The standard commercial license includes a covenant-not-to-sue scoped
to the licensed `bhdr-oss` deployment for VaultBytes patents reading
on the licensed code. Standalone patent licenses for non-`bhdr-oss`
use (clean-room ports, hardware accelerators, third-party FHE
libraries) are negotiated separately under
[LICENSE-PATENT.md](LICENSE-PATENT.md).

**What about trademarks?**
"BHDR", "CipherExplain", and "VaultBytes" are trademarks of
VaultBytes Innovations Ltd. The commercial license does not grant
trademark rights beyond reasonable nominative use ("powered by BHDR").
Co-branding is negotiated separately.

**Can I get pricing without contacting sales?**
Not at this time. Pricing depends on deployment scope, required
support level, and whether a standalone patent license is included. It
is confirmed in writing per quote.

---

Product (CipherExplain SaaS, on-prem, OEM): [cipherexplain.com](https://cipherexplain.com)
Kernel commercial licensing contact: **b@vaultbytes.com**
