# Ferrara run-to-failure dataset: source review

Status: metadata inspected; native files not downloaded or qualified. Owner: Dr. Moore. Review date: 2026-10-11.

The supplied temporary URL identifies [Part 2, version 1](https://data.mendeley.com/datasets/zz8hpyx939/1), DOI 10.17632/zz8hpyx939.1. Its signature expired October 9, 2026 at 18:41:05 UTC. Signed credentials are not retained in repository records. Related [Part 1](https://data.mendeley.com/datasets/htk59pp5wx/1), DOI 10.17632/htk59pp5wx.1, belongs to the same campaign; do not count the two parts as independent campaigns.

The source attributes the dataset to Alberto Gabrielli, Luca Arpa, Mattia Battarra and Emiliano Mucchi at the University of Ferrara, published April 22, 2024, under CC BY 4.0. Preserve attribution, license and change notices.

The campaign describes six accelerated trials using 1205 ETN 9 bearings, fixed speed/load within each trial, and radial acceleration in MAT files. Reproduction instructions specify 5-second captures every five minutes at 25.6 kHz, with stopping at a 20 g acceleration peak. End-of-test observations report outer-race defects. The general description calls capture continuous, conflicting with those acquisition intervals; resolve against native timing evidence.

## Required engineering checks

Inventory both parts and establish their run membership before splitting. Verify checksums, actual MAT variable names, numeric units/calibration, signal dimensions and sample rates. The nominal expected window size is 128,000 samples, a calculation rather than an inspected fact. Do not reuse LDM-UPB calibration or IMS channel mappings.

Record actual speed/load values, missing windows and timestamps. A threshold-defined stop is not demonstrated physical failure time or fault onset. Define the forecast event and censoring policy before generating RUL targets. Separate all windows of each physical bearing/run before fitting preprocessing; the two archive parts are not train/test labels. Native data integrity, part completeness, intended-use review, independent performance and customer-site transfer remain unresolved.

Trace: PULSE-FR-001/002 source integrity and contracts; PULSE-FR-004/005/006 target eligibility; PULSE-NFR-008 group separation; AIG-REQ-001 version trace. No training, Azure action or gate promotion occurred. This record is source review, not runtime validation.
