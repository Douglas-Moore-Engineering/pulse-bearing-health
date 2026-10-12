# SCA case 1 envelope-feature development

Exploratory development only; no detector promotion. The documented shaft-Hz interpretation of the inner-ring feature detected **112/117 fault snapshots (95.73%)**, missed five, and flagged **7/126 normal snapshots (5.56%)** on the other placement. The RMS comparison detected 1/117 with 0/126 normal positives. These are snapshot results from one case, not independent bearing or operating-day rates.

[Reproducible program](../../scripts/evaluate_sca_spectral.py) and [complete results](../../governance/evidence/sca-case1-spectral.json) retain all six feature/placement combinations under each of two frequency interpretations. No only-best-result filtering is applied to the evidence. Run with SciPy and NumPy available using `python scripts/evaluate_sca_spectral.py`.

## Method

Reverified case 1 publisher hashes. Demean each waveform, compute the unfiltered Hilbert amplitude envelope, remove its mean, and calculate a Hann-windowed power spectrum. For up to three in-band harmonics, compare mean power inside a +/-2% frequency band (minimum two Fourier bins) with surrounding power at two to four band widths. Average harmonic contrasts. Multiply shaft speed by the supplied fault multiple and calibrate each feature/placement separately at the 99th percentile of normal publisher-train scores. No fault test labels are used to fit that percentile. Exclude label -1 and invalid speed.

This is a feature investigation, not a frozen independent test. The source fault type is already known, so presenting the inner-ring result as a selected general-purpose detector would be optimistic. A future multi-fault decision must explicitly combine features and measure the resulting false-positive rate; do not sum overlapping per-feature counts. Speed normalization of target frequency does not establish amplitude invariance across speed/load.

## Frequency and coverage limitations

The paper describes multiples of shaft speed in Hz. The native coefficients are unusually small, so the experiment also reports an RPM-coefficient hypothesis rather than silently changing units. The alternative inner/outer-ring interpretation is mostly outside the 320 Hz Nyquist limit: only one normal calibration record and two test records per placement yield those features. Its tiny denominators make its percentile/results unsuitable for a detector. Do not count out-of-band records as true negatives. The documented interpretation remains the reproducible reported basis, but physical frequency interpretation requires source clarification or independent bearing-geometry verification before a mechanistic fault claim.

Both approaches use unfiltered envelopes; carrier-band choice and available bandwidth remain development questions. The SCA labels were themselves assigned partly by envelope-spectrum analysis, so agreement is not equivalent to independent physical-inspection validation.

## Verification and disposition

A synthetic amplitude-modulated carrier check verified that the feature at the known modulation frequency exceeds an off-frequency feature by more than 100x; an above-Nyquist target returns unavailable. This checks signal-processing behavior, not diagnostic accuracy. Native input checks and full experiment completed successfully.

Case 1 remains development data. Cases 2-11 remain uninspected. Retrospective post-replacement calibration, left-censored fault onset and unverified continuous operating exposure still apply. Next step is a frozen multi-fault decision and coverage policy, with asset-group leakage review, before reserved-case evaluation. Do not lower thresholds simply to remove the five misses. The deployed API and acceptance targets remain unchanged; **NOT_PROMOTED**.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Model engineering owns development and source-unit verification; domain/release reviewers retain qualification authority.
