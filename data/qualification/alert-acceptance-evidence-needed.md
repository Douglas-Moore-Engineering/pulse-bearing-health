# Evidence needed to score the alert acceptance targets

This specification fills the measurement gap identified by the research replays. It does not change the fictional 60-minute warning or one-nuisance-episode-per-bearing-per-30-operating-days targets, and does not require discarding the current public datasets.

## Warning evidence

Each scored bearing needs a stable bearing/run ID, a defined event (for example a documented intervention threshold rather than unspecified physical failure), the event timestamp or explicit uncertainty interval, source provenance and time basis. Acquisition timestamps must use the same clock or a documented conversion. Preserve operating/rest periods. A last recording alone is a proxy; it is not automatically the event timestamp. Any change to the accepted event definition must be labeled a requirements change, not silently applied after detector results are known.

## Nuisance evidence

Use intervals with independently supported bearing condition and recorded operating exposure. Retain bearing identity, interval start/end, timezone or clock basis, active operating time, speed/load regime, maintenance/inspection observations and confidence/limitations of the condition label. Neither low RMS nor membership in the initial reference window proves health: using the candidate itself to establish its negative labels would be circular.

Retain every candidate alert with first/last timestamps, episode ID, bearing ID and the frozen episode/reset policy. Review outcomes may be confirmed degradation, confirmed nuisance or unresolved. Unresolved events remain separate. Count episodes rather than signal windows or sensor channels; deduplicate neither bearings nor long intervals without an explicit rule. Report total verified healthy operating exposure and uncertainty alongside a rate. Short healthy intervals can be useful, but an unsupported extrapolation to 30 operating days cannot pass acceptance.

## Current disposition

Current datasets support native-signal processing, development, and descriptive final-acquisition lead. Exact event labels and verified healthy exposure remain insufficient for the two operational acceptance claims. UNSW Tests 3/4 remain reserved pending useful endpoint/timing qualification. LDM final-test observations may guide a later development revision only after acknowledging their consumed status; they cannot be reused as fresh held-out evidence.

No site access, external author contact or customer communication is implied by this specification. No production approval is manufactured for the fictional customer.
