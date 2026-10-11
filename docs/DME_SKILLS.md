# DME skills in VS Code

Repository skill bundle v1 · 2026-10-11 · Five complete DME packages

The Pulse repository now carries its DME workflows, references, metadata, and diagram assets. The earlier pre-Azure package did not include these files, which explains why a separate VS Code session could not discover or name the expected skills.

## Expected inventory

| Skill name | Responsibility | Repository entry point |
|---|---|---|
| `customer-delivery-service-operations` | Customer lifecycle, scope, lifecycle cost, review and service handoff | [SKILL.md](../.agents/skills/customer-delivery-service-operations/SKILL.md) |
| `systems-engineering-standards-assurance` | Standards applicability, tailoring, SEMP and assurance | [SKILL.md](../.agents/skills/systems-engineering-standards-assurance/SKILL.md) |
| `build-production-ai-systems` | Technical design, engineering structure and delivery | [SKILL.md](../.agents/skills/build-production-ai-systems/SKILL.md) |
| `ai-governance-and-assurance` | AI lifecycle risk, oversight, evidence and authorization | [SKILL.md](../.agents/skills/ai-governance-and-assurance/SKILL.md) |
| `dme-diagram-standard` | Approved Mermaid visual standard and rendering assets | [SKILL.md](../.agents/skills/dme-diagram-standard/SKILL.md) |

Customer delivery coordinates the engagement. Standards assurance and AI governance apply across the lifecycle; technical engineering follows the governed handoff; diagram work invokes the diagram standard. Start from the current [engineering handoff](../customer/07-pre-azure-engineering-handoff.md), not a new intake. [AGENTS.md](../AGENTS.md) supplies repository instructions and the current authorization boundary.

## Load in VS Code

1. Open the local `pulse-bearing-health` repository or `pulse.code-workspace`.
2. Pull the published update. With `main` checked out and local work safely preserved, `git pull --ff-only` updates without creating a merge. If it refuses because of conflicting/divergent work, resolve that deliberately; do not reset or discard files to force it.
3. Start a new Codex conversation in that workspace. Run `/skills` or type `$` in the Codex input to inspect the available skills. Confirm all five names above.
4. Codex detects skill changes automatically. If the list has not refreshed, restart Codex; closing and reopening VS Code is a straightforward option.
5. Ask: "Read AGENTS.md and docs/DME_SKILLS.md. Confirm all five DME skills are discoverable and their required references/assets are available. Read PROJECT_STATUS.md and the engineering handoff. Report the remaining pre-Azure work. Do not connect to Azure or provision anything."

Current official documentation describes `.agents/skills/` as the repository discovery location and `/skills` or `$` for explicit selection: [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills), checked 2026-10-11. Older material may mention `.codex/skills/`; this bundle uses the current documented path. Do not duplicate the same packages into multiple discovery locations as a troubleshooting shortcut.

If a skill is still missing, confirm the current branch includes this update and the repository files exist, check any explicitly disabled-skill configuration, and record the affected exact names. Files on disk alone are not evidence that an IDE session has discovered/enabled them. General Azure or architecture skills do not replace DME's workflows.

## Provenance and maintenance

[The package manifest](../.agents/skills-manifest.json) records the source skill-workspace Git commit and SHA-256 of every bundled file. The initial copy preserves all source files byte for byte, including the approved diagram reference image; no workflow content was rewritten for this installation. These repository copies are a pinned snapshot and do not automatically synchronize with future edits in ChatGPT.

For an authorized update, compare the full authored package, preserve required references/assets, review the diff, update source provenance and file hashes, and commit the package and manifest together. Avoid editing the same skill independently in two places without reconciling the change.

Run `python scripts/validate_review_package.py` for offline inventory, hash, link, and existing design checks. Passing proves those checks only. Discovery on Dr. Moore's VS Code installation must be confirmed there. Skill installation does not close the architecture backlog, qualify data, approve costs, authorize Azure, or establish production readiness.
