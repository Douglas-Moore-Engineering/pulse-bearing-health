# Security, Trust Boundaries and Threat Model

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Trust boundaries: public/user files → controlled reference workstation → future approved cloud workspace → evidence viewer; future OT collection through read-only intermediary is separate and unbuilt. No reference component can command equipment or submit real maintenance work.

Assets: source provenance, trained artifacts, customer/site data if later introduced, identities, cost budget and decision evidence. Adversaries/failures include corrupt source files, malicious pickle/model payloads, leaked secrets, excessive privileges, artifact/evidence tampering, denial of service and operational misuse. See [threat register](../governance/threat_register.csv).

Proposed controls: schema/size/units validation; integrity manifests; approved safe artifact formats and dependency scans; organization identity with managed workload identity; no embedded keys; RBAC scoped by environment; private data/artifact access; evidence with version/time/actor; immutable source and release digests; bounded workload and cost monitoring. No implementation or penetration test is claimed.

Future platform RBAC: Dr. Moore's named operator deploys only within a designated nonproduction resource group; workspace workload identity gets only required scoped data/secret permissions; readers cannot deploy; reviewer identity and protected promotion are separate where required. Actual identity/object IDs and assignments are TBD. Never grant subscription Owner just for convenience.

Prefer private inbound access and deny anonymous storage. Define operator network route/DNS before disabling public endpoints in a deployable design; a private workspace with no tested client path is not usable. Managed outbound isolation and inbound Private Link are different controls. No private network, endpoint or role has been created here. Site security and any IEC 62443 obligations require actual IT/OT review.

Log security metadata and decisions without raw waveforms, secrets or personal identifiers by default. Decide logging retention/access and incident responsibilities before cloud entry. Hardened code scanners and branch protection are planned, not currently verified.
