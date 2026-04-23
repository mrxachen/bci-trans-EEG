# Repository Bootstrap

## Repo Identity
- GitHub repository: `bci-trans-EEG`
- Local Python package name: `bci_trans_eeg`
- Research focus: Phase I cross-device EEG motor imagery benchmark and device-aware adaptation

## Why This Skeleton Exists
- Create a stable engineering base before implementing adapters and experiments.
- Keep the repository aligned with the benchmark-first, config-driven plan from the project documents.
- Make future work easy to map from research question to module, config, and experiment output.

## Recommended Next Build Order
1. Add a formal dataset metadata schema and adapter base class.
2. Define protocol generation for zero-shot and few-shot evaluation.
3. Implement preprocessing presets and channel mapping policies.
4. Add baseline runners and evaluation summaries.
5. Add device-aware modeling modules after the benchmark path is stable.

## Expected Ownership Of Top-Level Areas
- `src/bci_trans_eeg/data/`: dataset registry, adapters, metadata, channel inventories
- `src/bci_trans_eeg/preprocessing/`: signal cleaning and canonical preprocessing rules
- `src/bci_trans_eeg/protocols/`: split definitions and calibration policies
- `src/bci_trans_eeg/models/`: baseline and method implementations
- `src/bci_trans_eeg/evaluation/`: metrics, reports, and result packaging
