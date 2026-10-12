# SCA localization metadata and timing audit

Consumed cases 1/2/11 only. [Reproducible audit](../../scripts/profile_sca_pairing.py) checks publisher hashes, extracts native sensor/bearing identities and matches timestamps using mutual nearest neighbours. [Evidence](../../governance/evidence/sca-pairing-profile.json). Pairing is a feasibility calculation, not proof of simultaneity, stable conditions or transmitted vibration. Explicit timestamp offsets are parsed; naive timestamps retain a same-clock assumption. Mixed aware/naive streams are rejected.

## Resolved context

Case 2 identifies the fault origin as DS, with **SKF6310 on DS and SKF6209 on FS**. Their supplied frequency coefficients differ; the implementation already uses each placement's own coefficients. Thus an accidental shared-bearing coefficient is not the explanation for case 2's false positives. Physical manufacturer verification remains outstanding.

Case 1 identifies SKF22320 E at both placements; its unusually small coefficients remain unresolved. Case 11 v2 uses native **id 14**, not 11, and SKF6226 at both placements. Preserve the mapping from publisher folder 11 to native id 14; do not join this case to another record solely by folder number. The publisher's v2 correction supersedes the paper's original case-11 setup.

## Paired coverage

| Test case | DS records | FS records | Mutual nearest pairs within 60 seconds |
|---|---:|---:|---:|
| 1 | 124 | 135 | 110 |
| 2 | 94 | 296 | 91 |
| 11 | 19 | 19 | 19 |

Case 2's median separation across all 93 mutual-nearest test pairs is 2.74 seconds. Only 91/296 FS snapshots have a mutual DS neighbour within 60 seconds. A paired detector would leave 205 FS records without such a partner; silently discarding those records would misrepresent coverage. The 60-second window is a reported sensitivity bound, not an accepted operational pairing requirement.

## What remains unknown

The inspected paper says actual load/noise levels were unknown (section 4.2). The inspected native fields do not provide a load history, mounting-change record or independent transmission measurements. Generic asset descriptions and bearing model names do not uniquely identify machines across cases. No new raw signals can be assumed to fix these annotation gaps.

The next implementable development experiment is a paired-sensor spectral comparison with explicit unmatched-record abstention, using only consumed data. It must not choose the known damaged side from `faultOrigin` during inference. Pair matching alone is not an improved detector, and current evidence does not establish bearing localization. Cases 3-10 remain reserved. No deployed code, threshold or release decision changed; NOT_PROMOTED.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001.
