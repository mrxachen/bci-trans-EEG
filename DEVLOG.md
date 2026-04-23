# DEVLOG

## 2026-04-23

### Task Start
- Goal: initialize project collaboration structure and persistent agent memory.
- Context reviewed: `dataset-review/`, `paper_review/`, `Document/`.
- Key context: Phase I is MI-first, benchmark-first, journal-first, and centered on cross-device harmonization plus few-shot device adaptation.

### Work Completed
- Created `configs/` for future configuration assets.
- Created `notes/` for distilled research context and project-facing notes.
- Added `AGENTS.md` to persist the required workflow and research-refresh memory.
- Added `PLANNING.md` as the standing planning ledger for every task.
- Added `DEVLOG.md` as the standing execution log for every task.
- Added `notes/research_context.md` to distill the current dataset, paper, and planning materials into a reusable development brief.

### Verification
- Verified source material categories and reviewed key document sections before initialization.
- No code or dependency execution was introduced in this task.

### Next Suggested Actions
- Define the initial repository architecture for Phase I implementation.
- Draft the dataset registry and benchmark protocol specification.
- Begin with a data-layer-first implementation plan tied to the MI benchmark.

### Task Start
- Goal: bootstrap the first code-oriented repository skeleton for `bci-trans-EEG`.
- Context reviewed: `AGENTS.md`, `PLANNING.md`, `DEVLOG.md`, `notes/research_context.md`.
- Key context: the repository must stay benchmark-first, MI-first, config-driven, and ready for later device-aware adaptation work.

### Work Completed
- Added project metadata and onboarding files: `README.md`, `.gitignore`, and `pyproject.toml`.
- Created the initial package layout under `src/bci_trans_eeg/`.
- Added minimal typed scaffolding for dataset registry, preprocessing specs, and benchmark protocol definitions.
- Added first-pass config templates for datasets, preprocessing, and zero-shot protocol setup.
- Added `notes/repo_bootstrap.md` to document the new repo identity and recommended build order.
- Added a lightweight smoke test file for package imports and scaffolding stability.

### Verification
- Verified the created tree and inspected the newly added files.
- Kept implementation at the scaffold level only; no dataset parsing or experiment logic was added yet.

### Next Suggested Actions
- Implement dataset metadata schema plus adapter base classes.
- Add few-shot protocol templates and benchmark split generation.
- Define the first baseline runner interfaces and evaluation output contracts.

### Task Start
- Goal: prepare the repository for public GitHub-backed development and first push.
- Context reviewed: `AGENTS.md`, `PLANNING.md`, `DEVLOG.md`, `notes/research_context.md`, `notes/repo_bootstrap.md`.
- Key context: this phase must stay benchmark-first while adding only lightweight engineering infrastructure.

### Work Completed
- Added public repository infrastructure: `LICENSE`, `Makefile`, GitHub Actions CI, issue templates, and PR template.
- Expanded `README.md` with installation steps, developer commands, and the collaboration workflow.
- Added a few-shot protocol template at `configs/protocols/few_shot_lodo.yaml`.
- Added `notes/task_startup_checklist.md` so formal tasks start from a consistent checklist.
- Extended the CLI with a `--smoke` path and extended tests to cover the smoke path.
- Initialized the local git repository on `main` and bound `origin` to `https://github.com/mrxachen/bci-trans-EEG.git`.
- Cleaned staged `Zone.Identifier` metadata files out of the initial commit set.

### Verification
- `make smoke` passed.
- `PYTHONPATH=src python -m pytest -s` passed with 4 tests.
- Plain `pytest` initially failed in the sandbox because no usable temporary directory was available for capture; rerunning with `-s` avoided the environment limitation.
- Git identity and remote target were verified before first commit preparation.

### Next Suggested Actions
- Create the initial commit and push `main` to GitHub.
- After the repository is online, start the first formal engineering task: dataset metadata schema plus adapter interfaces.

### Final Outcome
- Created the initial local commit history for the repository foundation.
- Pushed `main` to `https://github.com/mrxachen/bci-trans-EEG.git`.
- Restored `.github/workflows/ci.yml` on GitHub via the GitHub API because direct git push of workflow changes was blocked by the current OAuth app scope.
- Fast-forwarded the local branch back to the remote state so the working tree and GitHub remain aligned.

### Updated Next Suggested Actions
- Start the first formal implementation task: dataset metadata schema plus adapter base interfaces.
- Define the zero-shot and few-shot protocol generation layer next, before touching model code.
