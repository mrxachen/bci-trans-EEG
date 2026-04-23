# PLANNING

## Project Snapshot
- Theme: cross-device EEG fusion for innovative BCI methods research.
- Current phase: Phase I, journal-first, focused on motor imagery EEG.
- Immediate research line: standardized cross-device MI benchmark, strong baselines, and explicit device-aware few-shot adaptation.

## Standing Workflow
1. Read `AGENTS.md`, this file, and `DEVLOG.md` at the start of every task.
2. Refresh research context from `notes/research_context.md` and, when needed, the relevant source documents under `dataset-review/`, `paper_review/`, and `Document/`.
3. Update this file before execution with the task objective, scope, planned edits, and validation steps.
4. Update `DEVLOG.md` after execution with outcomes, evidence, and follow-up work.

## Current Approved Structure
- `configs/`: project and experiment configuration entry points.
- `notes/`: distilled research context, conventions, and future task-facing notes.
- `dataset-review/`: dataset survey sources.
- `paper_review/`: paper and method survey sources.
- `Document/`: expert discussion outputs, phase plans, and method derivations.

## Current Priorities
- Convert prior review materials into actionable engineering context.
- Stand up stable project conventions before code implementation.
- Keep every future development task tied to the benchmark-first Phase I route.

## Current Task
- Date: 2026-04-23
- Goal: bootstrap the first repository skeleton for the new GitHub repo `bci-trans-EEG`.
- In scope: project metadata, package layout, config templates, notes, and test scaffolding.
- Files expected to change: `README.md`, `.gitignore`, `pyproject.toml`, `src/`, `configs/`, `notes/`, `tests/`, `DEVLOG.md`.
- Validation plan: verify the generated tree, inspect key files, and confirm the package imports and config files are structurally aligned with the benchmark-first route.
- Research documents to revisit: `notes/research_context.md`, `Document/phase1_github_code_development_plan.md`, `Document/phase1_overall_implementation_plan.md`.

## Current Task
- Date: 2026-04-23
- Goal: prepare the repository for public GitHub-backed Phase I development.
- In scope: git initialization, MIT license, CI, GitHub collaboration templates, few-shot config template, developer command entrypoints, and public-facing documentation polish.
- Files expected to change: `README.md`, `.gitignore`, `pyproject.toml`, `Makefile`, `.github/`, `configs/protocols/`, `notes/`, `tests/`, `DEVLOG.md`.
- Validation plan: run local smoke tests, run `pytest`, verify git status and remotes, and confirm the first push target is `mrxachen/bci-trans-EEG`.
- Research documents to revisit: `notes/research_context.md`, `notes/repo_bootstrap.md`, `Document/phase1_github_code_development_plan.md`.

## Open Near-Term Tasks
- Define the initial codebase layout for data adapters, preprocessing, protocols, baselines, and evaluation.
- Turn the MI four-dataset strategy into a concrete dataset registry and protocol definition.
- Translate the current method direction into implementable modules and experiments.

## Task Start Template
- Date:
- Goal:
- In scope:
- Files expected to change:
- Validation plan:
- Research documents to revisit:
