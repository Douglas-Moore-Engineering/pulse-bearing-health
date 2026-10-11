# Approved DME visual standard

Authority: Dr. Moore's explicit approval on October 1, 2026, following review of the transparent MHFF grouped architecture preview. That approved preview, rather than earlier rectangular/oval pipeline experiments, is the visual reference.

## Layout and shape rules

Use a vertical, grouped Mermaid architecture. Put real components inside named functional or responsibility groups. Draw labeled component-to-component connections, with lateral branches and clear convergence where the system requires them. Keep group outlines thin, backgrounds unfilled, and labels clear of nodes and edges. Prefer short group headings.

Use squared-corner component rectangles, database cylinders, and genuine decision diamonds. Preserve exclusive and concurrent execution semantics. Use curved connectors by default. Do not force four branches or copy the model-candidate layout from the earlier unapproved experiment.

## Fixed color-role mapping

| Color | Role | Fill | Stroke |
|---|---|---|---|
| Blue | Customer/source systems, plant/OT, source records | `#EAF3F8` | `#356079` |
| Teal | Data foundation, contracts, quality, ingestion, governed data | `#E5F4F2` | `#32746E` |
| Indigo | Features used for modeling, analytics, AI/ML services | `#EDF0FA` | `#42558B` |
| Gold | Policy, governance, eligibility, decision guardrails | `#F8F2E4` | `#876A2D` |
| Green | People, authorized human decisions and operations | `#EFF6EB` | `#4C713E` |
| Purple | Evidence, provenance, evaluation records, audit and outcome ledgers | `#F3F0F8` | `#6E5B85` |
| Rose | Security, threat controls and security-response components, when used | `#FBEFED` | `#9B534C` |

Use text `#111111` and connectors `#425466`; typical node/group strokes are 1.5–2 px. Use Arial or a metrically similar sans-serif consistently. These role mappings govern a whole project; do not recolor a role differently in adjacent views.

Include a visible legend for the colors actually used, with color names and semantic role labels. The legend may sit beneath the diagram in an export/document wrapper. It must not be omitted from the user-visible artifact merely because the source includes color comments. Keep explanatory words, not just colored swatches.

## Background and export

Set the canvas and group fills to transparent/none. Keep node fills so the semantic colors remain visible. Remove filled outer panels, decorative textures, and colored lane backgrounds. Export PNG with an alpha channel and transparent background pixels; preserve transparency in SVG. Retain group outlines and titles. Inspect on a light surface for legibility without flattening that surface into the delivered image.

The user-approved PNG has dark labels intended for a light viewing/document surface. Do not mistake a viewer's black transparency matte for a requested black background. Do not introduce an opaque image background to compensate without a new user instruction.

For PDF/DOCX delivery, preserve portrait US Letter and one coherent view per page where practical. The page may be white; the embedded diagram must remain transparent. Split dense views into named companion views while keeping the same style.

## Reference and reproducibility

- `../assets/approved-mhff-reference.png`: exact user-approved rendered appearance, including its legend.
- `../assets/approved-mhff-reference.mmd`: its source and semantic color assignments.
- `../assets/architecture-template.mmd`: reusable scaffold, not a mandatory system topology.
- `../assets/mermaid-config.json`: renderer settings matching the approved reference, including smaller group headings to avoid the observed heading overlap.

The approved source describes a proposed MHFF architecture, not deployed software. Treat its content only as an example. Keep real project sources, requirements, and validated logic authoritative. Preserve the established full diagram inventory; a style standard does not replace as-is, to-be, data, security, deployment, or other required views with one generic chart.
