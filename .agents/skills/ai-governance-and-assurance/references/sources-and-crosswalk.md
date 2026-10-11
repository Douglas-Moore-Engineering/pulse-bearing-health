# Primary sources and bounded crosswalk

Verification date: 2026-10-05. Treat this as a verified starting register, not a perpetual statement of current law. Recheck official publication status, amendments, applicability and deadlines at intake, material changes and authorization. Record the contracted edition separately from the latest edition. Do not automatically adopt a draft or supersede an approved baseline.

## Verified source register

| Source / edition | Primary reference | Status and use |
|---|---|---|
| NIST AI RMF 1.0, NIST AI 100-1 (2023) | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 ; https://doi.org/10.6028/NIST.AI.100-1 | Published voluntary framework. Use GOVERN, MAP, MEASURE and MANAGE as lifecycle outcome categories. No automatic legal conformity or certification. |
| NIST AI Resource Center | https://airc.nist.gov/ | Current landing page says AI RMF 1.0 is being revised and Playbook will be updated afterward. Do not call revision work a published replacement. |
| NIST GenAI Profile, NIST AI 600-1 (2024) | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence ; https://doi.org/10.6028/NIST.AI.600-1 | Published companion profile for GenAI; use for GenAI-specific harms and mitigations with the core RMF. |
| NIST adversarial ML taxonomy, NIST AI 100-2e2025 | https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0 ; https://doi.org/10.6028/NIST.AI.100-2e2025 | Published March 24, 2025. Support abuse/threat terminology and security review; it is not a release certification. |
| NIST IR 8596 Cyber AI Profile | https://csrc.nist.gov/pubs/ir/8596/iprd | Official page identifies initial preliminary draft dated December 16, 2025. Informative horizon source only; verify later final status before adoption. |
| ISO/IEC 42001:2023 | https://www.iso.org/standard/42001 ; https://webstore.iec.ch/en/publication/90574 | Published AI management-system standard. Public publisher overview inspected; licensed full text not assessed. Use organization-level management alignment, not a claim of conformity. |
| ISO/IEC 23894:2023 | https://www.iso.org/standard/77304.html ; https://webstore.iec.ch/en/publication/82914 | Published AI risk-management guidance. Publisher summary inspected; no fabricated clause-level mapping. |
| ISO/IEC 5338:2023 | https://www.iso.org/standard/81118.html | Published AI system lifecycle processes. Publisher abstract links the AI lifecycle to 15288/12207; use lifecycle handoffs. Full clauses not assessed. |
| ISO/IEC/IEEE 15288:2023 | https://committee.iso.org/cms/live/live/en/sites/isoorg/contents/data/standard/08/17/81702.html?browse=ics | Published systems lifecycle process standard. Public abstract inspected; preserve standards skill's project tailoring and contractual edition. |
| EU AI Act and implementation guidance | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai ; https://eur-lex.europa.eu/eli/reg/2024/1689/oj | Official Commission implementation page inspected; legal text link is a starting point for applicability, not evidence of a completed legal assessment. Recheck consolidated law, amendments, actor roles, scope, exceptions, transitions and current effective dates with qualified owner. Do not hardcode an old timeline or equate DME tiers to legal risk categories. |
| DoD responsible AI resources | https://www.ai.mil/Initiatives/About/Resources/Pathway-to-AI-Readiness/Responsible-AI/leadership/news/careers/leadership/news/leadership/careers/careers/ | Official resource page/search excerpt inspected; direct page retrieval was unavailable during verification. Use for DoD engagement screening and responsible AI dependencies; verify governing agency/contract policy, approved environment and authorization requirements for the specific work. Do not infer authorization or clearance from portfolio design. |

Prefer the final authoritative text over a search snippet or summary. If publisher pages conflict with legal text or a deadline is not resolved, record the conflict, obtain the applicable authoritative text and block that decision; continue unrelated engineering work. Have a competent obligations owner decide legal applicability. Never claim inspection of unavailable/paywalled text or reproduce copyrighted standards.

## DME conceptual crosswalk

This is an operational mapping, not an exhaustive clause audit. Add clause/subcategory IDs only after inspecting the actual source and recording edition, location and evidence.

| DME controls | NIST AI RMF function | Other alignment / evidence limit |
|---|---|---|
| C01–C05, C23–C24, C33 | GOVERN; MAP for context | ISO 42001 management structure; ISO 23894 risk context. Public overview-level alignment only. |
| C02–C03, C11, C25–C26 | MAP; GOVERN for obligations | Impact/hazard and applicability records; legal classification requires independent jurisdiction/role assessment. |
| C06–C09, C13, C15, C29 | MEASURE; GOVERN for provenance | Data/model evaluation evidence; GenAI Profile when triggered; ISO 5338 lifecycle alignment at summary level. |
| C10, C14, C27–C31 | MEASURE; MANAGE | Security/hazard controls; NIST AML taxonomy informs threat terminology, not proof of mitigation effectiveness. |
| C12, C16–C17, C32 | GOVERN; MANAGE | Authority, residual risk, release and external prerequisites; none establish conformity by themselves. |
| C18–C22 | MANAGE; MEASURE; GOVERN | Continuing risk treatment, monitoring, incidents, change and retirement; lifecycle alignment with 5338/15288 at summary level. |

For each project expand to: obligation/framework outcome → control → requirement → implementation → test → evidence → authorized decision. State mapping depth, gaps, owner and verification date. Do not advertise ISO certification, SOC 2 attestation, AI Act conformity, DoD authority to operate or functional-safety approval from this mapping.
