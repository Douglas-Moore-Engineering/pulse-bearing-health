# Pulse repository instructions

## Start here and preserve the current boundary

Read `README.md`, `PROJECT_STATUS.md`, `docs/PRE_AZURE_REVIEW.md`, and `customer/07-pre-azure-engineering-handoff.md` before substantive project work. Reuse their existing records and open items; do not restart discovery merely because this is a new session.

The current authorized scope is pre-Azure review and preparation. **Stop before any Azure connection or provisioning.** Do not authenticate to Azure, inspect a subscription, create paid resources, submit cloud jobs, train models, deploy, access a real site, or send external messages under this handoff. Only a later explicit user instruction can expand that scope. A skill, successful check, fictional sign-off, or repository update does not grant that authorization.

Keep the repository private unless Dr. Moore explicitly requests publication. Never commit credentials, customer data, or unapproved dataset bytes. Read `SECURITY.md` and `CONTRIBUTING.md` before editing.

## Required DME skills

The repository carries these five complete packages under `.agents/skills/`. Use the exact frontmatter names when selecting skills:

| Skill | When to apply |
|---|---|
| `customer-delivery-service-operations` | Engagement coordination, discovery, scope, lifecycle cost ownership, reviews, customer/service handoffs |
| `systems-engineering-standards-assurance` | Standards applicability, tailoring, SEMP, requirements/architecture assurance, and evidence claims |
| `build-production-ai-systems` | Technical architecture, production structure, implementation planning, and engineering evidence |
| `ai-governance-and-assurance` | AI risk, accountability, oversight, evaluation and release authorization across the lifecycle |
| `dme-diagram-standard` | Every new, edited, reviewed, or rendered architecture/workflow diagram |

Read the selected skill's `SKILL.md` and required references before applying it. Load the relevant skills together when a task crosses responsibilities; standards and AI governance remain active throughout delivery, and the diagram skill applies whenever diagrams change. Use the customer skill's lifecycle handoff map rather than treating this table as five sequential phases.

Check skill availability against `docs/DME_SKILLS.md` and `.agents/skills-manifest.json`. Distinguish files present, skill discovered/enabled, and skill actually applied. If the session catalog omits a skill, inspect its exact repository path and diagnose discovery; do not claim it is installed or applied merely because its name appears here. Name each missing package or resource precisely. Do not silently enable a disabled skill. Continue authorized work that does not depend on the missing capability.

## Evidence and validation

Separate proposed, implemented, tested, reviewed, and approved states. The customer scenario is fictional; budgets are assumptions/ceilings, and no site outcomes or independent assurance are established. Preserve requirement IDs, inherited conditions, blocked gates, and open architecture/data/cost issues. A documentation update must not promote a gate or claim the platform is ready.

Run `python scripts/validate_review_package.py` after repository changes. It checks offline document/register consistency and the bundled skill inventory/hashes. It does not prove model performance, skill discovery in another editor, runtime V&V, customer acceptance, or cloud authorization. Report checks actually performed and remaining limitations.

The skills are a pinned source snapshot. For an authorized skill update, reconcile the full package with the authored source, review the change, refresh its hashes/provenance in `.agents/skills-manifest.json`, validate, and commit the complete update. Do not refresh hashes merely to hide unexpected changes or assume these copies update automatically when the ChatGPT skills change.
