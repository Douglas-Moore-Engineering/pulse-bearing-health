# DME skill dependencies

Updated 2026-10-12. DME workflow packages are maintained in the installed skills workspace outside this project. The repository retains project-specific requirements, measurements, evidence and decisions. Historical bundle copies and their manifest have been removed from the current tree; Git history is preserved.

| Required skill name | Responsibility |
|---|---|
| `customer-delivery-service-operations` | Engagement, lifecycle cost, review and service handoff |
| `systems-engineering-standards-assurance` | Applicability, tailoring, SEMP and assurance |
| `build-production-ai-systems` | Architecture, engineering structure, implementation and measurement evidence |
| `ai-governance-and-assurance` | AI risk, oversight and authorization |
| `dme-diagram-standard` | Architecture/workflow diagram standard and rendering assets |

Resolve these exact names through the active environment's installed skill catalog and read the selected package's actual entry point and required resources. If a dependency is missing, report it and continue independent authorized work. Do not copy the reusable bundle back into the repository or assume that availability in ChatGPT proves availability in VS Code.

Start with [repository instructions](../AGENTS.md), [current status](../PROJECT_STATUS.md) and [demo handoff](../customer/10-demo-readiness.md). Historical pre-Azure documents remain design baselines; current user authorization governs the work actually permitted.

## Diagram rendering

`scripts/render_reference_views.cjs` requires `DME_MERMAID_CONFIG` to identify the absolute path to the approved `mermaid-config.json` in the externally installed diagram skill. Supply the temporary Mermaid tooling directory as its first argument and, optionally, a view name as its second. `PULSE_BROWSER` identifies the browser executable. The renderer checks the config exists before loading tooling or writing outputs. Existing diagram source and exports are unchanged by the skill cleanup.

## Repository checks

Run `python scripts/validate_review_package.py`. The check validates project records and rejects committed skill copies; it no longer requires a repository skill bundle. It does not verify IDE installation, measurement truth, approver identity or production readiness.
