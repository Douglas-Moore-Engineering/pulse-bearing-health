---
name: dme-diagram-standard
description: Create, edit, review, and render architecture and workflow diagrams for Dr. Moore and Douglas Moore Engineering using the approved Mermaid visual standard. Apply to system context, as-is and to-be architecture, data and AI pipelines, security, deployment, governance, operations, and documentation diagrams, including diagram-only requests and production-system builds.
---

# DME Diagram Standard

Apply the visual standard approved by Dr. Moore on October 1, 2026. Treat it as the default for DME and the user's professional diagram work. Apply it directly without asking the user to explain or approve the same visual format again. Follow a later explicit user change when one is given.

## Start from the approved reference

Before creating or restyling diagrams:

1. Read `references/visual-standard.md`.
2. Inspect `assets/approved-mhff-reference.png` and read its editable source, `assets/approved-mhff-reference.mmd`. View the transparent image on a light inspection surface when necessary; do not bake that inspection surface into the output.
3. Use `assets/architecture-template.mmd` and `assets/mermaid-config.json` as the reusable starting point. Adapt the system content and group names to the actual task.
4. Preserve valid architecture, requirements, source status, and execution semantics while changing presentation.

Use the approved reference's structural language: a top-to-bottom Mermaid architecture, explicitly named groups, individually colored components, directly connected nodes, and short labels explaining their relationships. A generic vertical list of boxes or a wide model-comparison pipeline alone does not reproduce the approved architecture format.

## Required presentation

- Author editable Mermaid `.mmd` source. Use `flowchart TD` or `flowchart TB` for architecture and process views.
- Use squared-corner rectangles for components, services, processing steps, and human-review steps. Use cylinders for actual data stores and diamonds for actual decisions. Do not substitute oval/pill components; that option was rejected.
- Use named `subgraph` groups to show responsibility, functional domain, ownership, lifecycle stage, or trust boundary where relevant. Retain thin group outlines and readable titles; leave group backgrounds unfilled.
- Keep the canvas transparent. Do not add an opaque white/dark panel, decorative background, dotted grid, background image, or filled swimlane bands. A document page or viewing surface may itself be white; the diagram must remain transparent.
- Apply the fixed semantic palette in `references/visual-standard.md` to nodes. Include a visible legend with both color names and architectural meanings. Preserve colors across related views.
- Connect components directly. Label significant edges with what is transferred, invoked, validated, recorded, or authorized. Use curved connectors by default; keep the primary flow vertical, branch sideways when needed, and route feedback loops clearly.
- Preserve genuine branching and convergence. Do not force every view into the same branch count, create decorative relationships, or conflate alternative decisions with parallel execution.
- Keep each view focused and readable. For document delivery retain portrait US Letter, 8.5 × 11 inches. Split dense content into additional linked views instead of shrinking text or switching to a different visual style.

For a sequence, state, ER, or other notation that communicates the needed relationship more accurately, preserve its correct semantics and use the same palette, background, typography, and legend discipline. Do not create a false workflow merely to force every diagram into a flowchart.

## Render and verify

Render precise diagrams from source. Do not use image generation to redraw their topology or text. When a user asks to see the result, show a rendered preview with the editable source available; raw code alone is not a substitute for the requested visual.

Inspect the rendered result against the approved reference. Check group-heading clearance, readable node and edge labels, arrow endpoints, branching, color meanings, and transparency. Verify an exported PNG has an alpha channel and transparent background pixels; ensure exported SVG and group styles do not introduce opaque background fills.

Keep a title, short purpose, view status, and legend with shared or client-facing diagrams. Distinguish assumed current state, proposed design, and verified implementation. Do not copy cloud products, repository links, filenames, benchmark names, or implementation claims from a style example into another system without evidence.

In a project repository, retain editable sources under `docs/diagrams/`, render them in the architecture documentation, and link the diagram index from the root README. Keep exports and source consistent. Do not claim that earlier diagrams were restyled unless those files were actually updated and reviewed.

Use this approved style for subsequent diagrams without another style-confirmation loop. Ask only about materially missing system information or a genuinely conflicting new instruction.
