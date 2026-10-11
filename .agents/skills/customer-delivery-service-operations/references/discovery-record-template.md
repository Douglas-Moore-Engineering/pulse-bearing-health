# Customer discovery record template

Copy into the customer's governed project workspace, adapting existing records instead of duplicating them. Replace bracketed prompts with answers or explicit Unknown/Not Applicable entries. Preserve the distinction between supplied facts and assumptions.

## Record metadata

| Field | Entry |
|---|---|
| Customer / organization | [Name] |
| Project / opportunity and record ID | [Name; e.g. DISC-001] |
| Version / date / timezone | [Version and effective date] |
| Engagement type | [Actual customer / Internal reference / Fictional portfolio] |
| Participants / roles / interviewer | [Names or role placeholders] |
| Owner / reviewer / decision authority | [Roles; Unknown where unassigned] |
| Classification / permitted storage | [Applicable handling and location] |
| Current lifecycle phase / authorized scope | [Phase and scope] |
| Explicit stop boundary | [User or engagement limit; None stated if absent] |
| Review state | [Draft / Prepared for Review / Reviewed with Customer / Fictional planning baseline] |
| Related existing records | [Paths/versions; None if new] |

## Interview coverage

Use response states Answered, Partial, Unknown, or Not Applicable with rationale. Record evidence state separately: Customer-stated, Source-inspected, Measured, Assumption, Fictional, or Conflicting. Link multiple supporting records rather than treating one verified sample as proof of all claims.

| Question | Response state | Response/evidence references | Owner / follow-up |
|---|---|---|---|
| Q-01 Problem and impact | [State] | [References] | [Owner/action] |
| Q-02 Success and acceptance | [State] | [References] | [Owner/action] |
| Q-03 Users and decisions | [State] | [References] | [Owner/action] |
| Q-04 Scope and data | [State] | [References] | [Owner/action] |
| Q-05 Hosting and restrictions | [State] | [References] | [Owner/action] |
| Q-06 Ownership and support | [State] | [References] | [Owner/action] |
| Q-07 Performance and recovery | [State] | [References] | [Owner/action] |
| Q-08 Budget and approvals | [State] | [References] | [Owner/action] |

### Repeat for each question or follow-up

- **Response ID / question:** [e.g. DISC-001-R01 / Q-01]
- **Customer response:** [Words or clearly labeled paraphrase]
- **Respondent / role / date:** [Source]
- **Evidence state:** [State]
- **Evidence supplied or requested:** [Artifact ID/path/version/date; access conditions]
- **Engineering interpretation:** [Derived meaning, not attributed as a customer statement]
- **Assumptions / contradictions:** [IDs and rationale; None if absent]
- **Response state:** [State, with rationale for Not Applicable]
- **Follow-up:** [Action, owner or owner-assignment action, due date or scheduling action]
- **Decision or gate affected:** [Scope, architecture, acceptance, access, build, etc.]
- **Downstream references:** [Requirement/acceptance/risk/decision IDs when assigned]

## Discovery summary and read-back

- Problem, impact and baseline evidence: [Summary]
- Users, workflow, decisions and authority: [Summary]
- Desired outcome and measurement: [Summary]
- In-scope and out-of-scope boundaries: [Summary]
- Sources, interfaces, hosting and constraints: [Summary]
- Ownership, service, training and exit expectations: [Summary]
- Budget, timing, dependencies and approval route: [Summary]
- Feasibility limits and unresolved information: [Summary]
- Customer corrections and read-back disposition: [Evidence/date or Pending; label simulations]

## Candidate requirements and acceptance trace

Preserve any existing project ID conventions. The examples below describe column content, not invented project commitments.

| Requirement ID | Atomic candidate statement | Source response/evidence | Rationale / owner / priority | Verification approach | Status / version | Acceptance ID |
|---|---|---|---|---|---|---|
| [SYS-xxx] | [The system shall ...; quantified only with a stated basis] | [DISC response IDs / evidence] | [Values] | [Inspection, analysis, demonstration or test] | [Candidate/version] | [AC-xxx] |

| Acceptance ID | Metric and unit / population | Baseline / source | Target / basis | Evaluation conditions and window | Evidence method | Acceptance authority / status |
|---|---|---|---|---|---|---|
| [AC-xxx] | [Definition] | [Value or Unknown] | [Proposed/agreed/TBD and rationale] | [Conditions] | [Planned evidence] | [Role/status] |

Reference existing stakeholder, source, responsibility, assumption and risk registers. Create separate records only when they improve ownership or review; a single governed document is sufficient for a small discovery engagement.

## Open items and decision record

| Item ID | Unknown, assumption, conflict or risk | Source | Impact / affected decision or gate | Owner | Follow-up / due date | Closure evidence / status |
|---|---|---|---|---|---|---|
| [OPEN-xxx] | [Description] | [Response/evidence] | [Impact] | [Owner or assignment action] | [Action/date or scheduling action] | [Pending or actual evidence] |

| Decision ID | Decision and alternatives | Basis / artifact versions | Authority | Actual, proposed or simulated | Date / conditions / review trigger |
|---|---|---|---|---|---|
| [DEC-xxx] | [Decision] | [References] | [Role] | [State] | [Values] |

## Handoff and continuation

- **Current phase and completed scope:** [Specific state, not entire-project completion]
- **Inputs and outputs:** [Versioned artifact references]
- **Receiving skill and responsible role:** [Exact skill name and person/role]
- **Inherited conditions and approvals:** [Actual evidence or explicitly simulated scenario]
- **Next permitted activity:** [Concrete activity within existing authorization]
- **Stop boundary:** [Explicit boundary carried forward]
- **Outstanding decisions:** [IDs, owners, impacts and required evidence]
- **Expected return evidence:** [What the next phase must produce]

## Review checks

- [ ] All eight core topics have a recorded disposition.
- [ ] Customer statements, inspected/measured evidence, assumptions and fiction are distinguishable.
- [ ] Scope, stakeholders, authority, constraints and candidate outcomes are captured.
- [ ] Requirements and acceptance candidates trace to sources; unresolved targets remain explicit.
- [ ] Open items have an owner or assignment action, follow-up and affected decision.
- [ ] The read-back and review state are recorded without invented approval.
- [ ] The next phase, receiving role, conditions and user stop boundary are preserved.

Completing this record establishes its documentation state. It does not establish technical feasibility, conformity, production readiness, or authority to spend or deploy.
