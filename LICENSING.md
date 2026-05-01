# Licensing

> **BHDR is one component of [CipherExplain](https://cipherexplain.com).**
> Most commercial users want the CipherExplain product, not a kernel
> license — go to [cipherexplain.com](https://cipherexplain.com) for
> SaaS, on-prem, or OEM terms. The licenses below cover the kernel
> source code and the underlying patent for the narrow set of cases
> where someone wants the kernel separately.

`bhdr-oss` is offered under three distinct, complementary licenses.
Pick the one that matches how you intend to use the kernel.

| License | Covers | Cost | Who it is for |
|---|---|---|---|
| **AGPL-3.0-or-later** | Source code copyright | Free | Researchers, AGPL-compatible deployments |
| **VaultBytes Commercial License** | Source code copyright, non-AGPL terms | Paid | Closed-source products, SaaS, regulated procurement |
| **VaultBytes Patent License** | PCT/IB2026/053405 method claims | Paid | Independent reimplementers, OEM embedders, field-of-use grants |

The three licenses are independent. The same Git tags are shipped to
all licensees. There is no closed-source build, no feature paywall, no
telemetry hidden in a proprietary fork.

---

## 1. AGPL-3.0-or-later (default)

You may use, study, modify, and redistribute `bhdr-oss` freely under
the standard AGPL terms:

- modifications you distribute must be released under AGPL-3.0-or-later,
- modifications you run as a network service that interacts with users
  must also be released under AGPL-3.0-or-later (the §13 network
  clause),
- every system that links against `bhdr-oss` must itself be
  AGPL-compatible.

The AGPL license grants no patent rights except to the minimum extent,
if any, expressly required by AGPL-3.0 itself. See
[LICENSE-PATENT.md](LICENSE-PATENT.md) for the patent position and how
to obtain a separate patent license.

If AGPL terms work for your deployment and you are not asserting the
patented method claims commercially, no further license is required.

See [LICENSE](LICENSE) for the full AGPL text.

---

## 2. VaultBytes Commercial License (paid)

A paid alternative to AGPL for deployments where AGPL is incompatible
with the licensee's product, customers, or procurement function.
Common cases:

- Embedding `bhdr-oss` in a proprietary product.
- Operating a hosted service (SaaS, internal portal, regulator console)
  where AGPL §13 source-disclosure is not acceptable.
- Linking `bhdr-oss` into a proprietary pipeline whose other
  components are not AGPL-compatible.
- A categorical procurement ban on AGPL dependencies (common in
  regulated banking, insurance, medical-device, and government supply
  chains).
- A requirement for contractual IP indemnity or service-level
  commitment for security patches, neither of which AGPL provides.

The standard commercial license bundles a covenant-not-to-sue scoped
to the licensed deployment for VaultBytes patents reading on the
licensed code. It does **not** automatically grant the standalone
patent license described below for non-`bhdr-oss` use.

See [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) for the terms.

---

## 3. VaultBytes Patent License (paid)

PCT patent application **PCT/IB2026/053405** covers the method —
non-interactive single-server Kernel SHAP under CKKS using compressed
coalition sampling — independently of the `bhdr-oss` source code.

A patent license is required if you implement the patented method in
your own code (a clean-room reimplementation, a port to a different
FHE library, or a hardware accelerator) and intend to use that
implementation commercially. The AGPL copyright license on this
repository does **not** grant patent rights for that case.

A patent license is also available as a field-of-use grant for OEM
embedders, FHE platform vendors, and regulated-industry deployments
that need standalone patent assurance separable from the source code.

See [LICENSE-PATENT.md](LICENSE-PATENT.md) for the patent terms,
eligibility, and how to obtain a license.

---

## Combining licenses

| Your situation | What you need |
|---|---|
| Want a deployable encrypted-SHAP product | [CipherExplain](https://cipherexplain.com) — not a kernel license |
| Read, fork, run tests, cite the paper | AGPL only |
| Internal AGPL-compatible deployment, no commercial assertion of method | AGPL only |
| Closed-source product or non-AGPL SaaS using this kernel source | Commercial license |
| Clean-room reimplementation of the method, used commercially | Patent license |
| Closed-source product **plus** clean-room ports of the method | Commercial + Patent license |
| OEM: embed the method in your platform under your own branding | Commercial + Patent license, typically with field-of-use scope |

CipherExplain customers receive patent coverage and non-AGPL terms as
part of the product license — they do not separately negotiate
kernel licenses. The kernel licenses on this page are for users who
explicitly want the kernel without the product.

When in doubt, contact **b@vaultbytes.com** before you deploy. A short
written confirmation is free and faster than a retrospective compliance
review.

---

## Trademarks

**BHDR**, **CipherExplain**, and **VaultBytes** are trademarks of
VaultBytes Innovations Ltd. AGPL forks inherit the source but may not
use the trademarks in their fork's name, marketing, or distribution
beyond reasonable nominative use ("powered by BHDR").

---

## Contributions

Outside contributions are not accepted. This keeps the copyright clean
and makes dual-licensing and the patent program possible. Customers
with custom-primitive requirements should raise them via the
commercial channel.

---

Licensing contact: **b@vaultbytes.com**
Security contact: see `NOTICE` and the paper.
