# Pulse repository instructions

## Start from the current evidence and authorization

Read `README.md`, `PROJECT_STATUS.md`, `customer/10-demo-readiness.md`, `docs/SKILL_COMPLETION_REVIEW.md`, `SECURITY.md` and `CONTRIBUTING.md` before substantive work. Preserve existing requirement IDs, evidence, open conditions and decisions. `customer/07-pre-azure-engineering-handoff.md` and `docs/PRE_AZURE_REVIEW.md` are historical design baselines; the current execution history is `customer/08-deployment-execution.md`.

The 2026-10-12 repository-maintenance task covers README, measurement/evidence, navigation and skill-placement corrections. It does not perform Azure access, provision resources, open reserved data, train a model, change a deployment, access a site or contact anyone. Respect explicit stop boundaries and use actual user authorization for subsequent work; documentation and fictional sign-off cannot grant authority.

Keep this repository private unless Dr. Moore explicitly requests publication. Never commit credentials, private backups, customer data or unapproved raw datasets.

## External DME skills

Resolve the exact names in `docs/DME_SKILLS.md` from the active installed skill catalog. Read the selected entry point and required resources. Maintain reusable skill instructions and assets outside the repository. Do not commit `SKILL.md`, `.agents/skills/`, `.codex/skills/` or a copied skill bundle elsewhere in the project. Verify availability in the actual executing environment; do not infer a VS Code installation from this file.

## Evidence and validation

Use `docs/appendix-a-kpi-dictionary.md` for definitions and `governance/measurements/README.md` for versioned measurement records. Preserve business need → KPI → requirement → implementation → measurement → evidence → decision. Keep missing outcomes not measured and report original denominators, independent units, evaluated versions and limitations. Historical reference evidence is not fresh runtime verification or customer acceptance.

Run `python scripts/validate_review_package.py` after repository changes. For runtime edits, also run the relevant software checks. Document/register consistency does not establish detector performance, independent assurance, customer approval or cloud authorization. Do not promote a gate solely through a documentation update.
