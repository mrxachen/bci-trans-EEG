# bci-trans-EEG

`bci-trans-EEG` is the Phase I research codebase for cross-device EEG motor imagery benchmarking and device-aware adaptation.

The repository is intentionally benchmark-first:
- standardize cross-device MI datasets and metadata
- define reproducible preprocessing and evaluation protocols
- establish strong baselines before method-heavy work
- support later device-aware few-shot adaptation research

## Phase I Scope
- Single-modal EEG only
- Motor imagery as the main paradigm
- Journal-first execution strategy
- Local-first experimentation on lightweight, reproducible components

## Phase I Goal
- build a standardized cross-device motor imagery benchmark
- establish reproducible preprocessing and evaluation protocols
- implement strong benchmark baselines before deeper method work
- create a stable foundation for explicit device-aware few-shot adaptation

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Development Commands
```bash
make help
make smoke
make test
```

`make smoke` is intended to validate the scaffold only. It does not run any dataset or training job.

## Repository Layout
- `src/bci_trans_eeg/`: Python package
- `configs/`: dataset, preprocessing, and protocol templates
- `notes/`: distilled research context and project-facing notes
- `scripts/`: task entrypoints and future automation hooks
- `tests/`: lightweight verification scaffolding
- `artifacts/`: generated outputs, logs, and result bundles

## Planned Development Order
1. Finalize dataset registry and metadata schema for the MI benchmark.
2. Implement data adapters and benchmark protocol generation.
3. Add preprocessing pipeline and baseline experiments.
4. Add device-aware modeling and few-shot adaptation modules.
5. Add reporting, reproducibility, and paper-facing result packaging.

## Collaboration Workflow
1. Read `AGENTS.md`, `PLANNING.md`, and `DEVLOG.md` before each task.
2. Refresh context from `notes/research_context.md` and relevant source materials.
3. Update `PLANNING.md` before implementation.
4. Update `DEVLOG.md` after implementation with verification evidence and next actions.

## Current Status
- Project conventions and agent memory are in place.
- The initial repository skeleton is ready for Phase I implementation.
- GitHub-ready project infrastructure is being prepared.
- No dataset adapters or experiments are implemented yet.
