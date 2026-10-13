# Security and Data Handling

Private reference system for a fictional customer. Consult [current status](PROJECT_STATUS.md) and [execution evidence](customer/08-deployment-execution.md) for the implemented boundary and unresolved controls; the original pre-Azure design is historical.

Never commit credentials, subscription secrets, customer operational/personal data, private backups or raw benchmark files without appropriate rights and authorization. Record approved locators and digests; do not commit signed access URLs. Keep the repository private unless publication is explicitly authorized.

Preserve advisory-only authority and read-oriented OT boundaries. Do not add machine-control writes, bypass equipment protection or convert reference output into a production diagnosis. Use the existing threat register, identity/access tests and release gates when changing controls. Recorded tests do not imply complete security assurance.

Report findings privately to Dr. Moore through an agreed channel. A repository instruction does not authorize external communication, Azure access, spending or production release.
