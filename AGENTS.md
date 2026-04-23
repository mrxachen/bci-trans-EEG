# Project Agent Memory

## Core Workflow
- Always start each task by reading `AGENTS.md`, `PLANNING.md`, and `DEVLOG.md`.
- Always update `PLANNING.md` at task start to record the current objective, intended scope, and near-term execution plan.
- Always update `DEVLOG.md` at task end to record what was done, what changed, verification status, and next actions.

## Research Context Refresh
- Before any development task, review the relevant research context from `dataset-review/`, `paper_review/`, and `Document/`.
- If the original materials are too large, read the distilled summary in `notes/research_context.md` first, then reopen the task-relevant original sections before coding.
- Do not start implementation with zero context refresh; at minimum, confirm the current task against the summary and the most relevant source documents.

## Current Research Direction
- Phase I is journal-first and benchmark-first.
- The current primary focus is cross-device EEG motor imagery research.
- The near-term target is a standardized cross-device MI benchmark plus an explicit device-aware few-shot adaptation method.

## Collaboration Constraints
- Keep changes small and reversible.
- Prefer config-driven and interface-first project evolution.
- Preserve a clear mapping from research question to code artifact, experiment, and paper contribution.
