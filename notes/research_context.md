# Research Context Summary

## Why This Project Exists
- The project targets cross-device EEG fusion and harmonization for BCI research, with the goal of producing publishable high-level methodology work.
- The current strategy is not to train a large foundation model first. It is to build a rigorous benchmark and a method with clear scientific contribution.

## Agreed Phase I Direction
- Focus on single-modal EEG motor imagery as the main line.
- Treat SSVEP and broader multimodal expansion as later-stage extensions, not the current main task.
- Optimize for a strong journal paper first, then expand toward stronger theory, larger data, and device deployment.

## Repeated Conclusions Across The Documents
- Benchmark-first is the safest and highest-value opening move.
- Cross-device evaluation must isolate device transfer from ordinary cross-subject or cross-session variation.
- Explicit device modeling is more valuable than generic black-box domain adaptation alone.
- Few-shot adaptation to a new device is a practical and publishable target.

## Dataset Review Highlights
- The most valuable resources are datasets with explicit device metadata and, when possible, same-subject multi-device recording.
- The review materials repeatedly emphasize that true same-subject multi-device public datasets are scarce.
- Public MI datasets remain the most practical starting point for Phase I benchmark construction.
- The broader dataset survey suggests using well-documented, device-traceable datasets and building a standardized metadata layer.

## Paper Review Highlights
- Existing work supports the feasibility of cross-device transfer, but device shift remains a real performance bottleneck.
- Prior methods cover statistical harmonization, spatial alignment, domain adaptation, and geometry-based alignment.
- The main research gap is that device effects are usually treated implicitly rather than modeled explicitly.
- Recent EEG foundation-model work improves heterogeneous-input compatibility, but does not remove the need for explicit device-aware modeling in small-data BCI settings.

## Planning Document Highlights
- `Document/phase1_overall_implementation_plan.md` sets the core deliverables:
  - Cross-device MI benchmark v1
  - Strong baselines
  - Device-aware core method
  - Reproducible codebase
- `Document/phase1_updated_journal_first_plan_v2.md` narrows the first paper target to a solid journal submission rather than a one-shot maximal theory paper.
- `Document/phase1_github_code_development_plan.md` argues for config-driven, local-first, benchmark-first, interface-first engineering.
- `Document/phase1_core_innovations_algorithm_derivation.md` frames the key contribution as explicit device factor modeling plus few-shot adaptation.
- `Document/deep_algorithm_research_diode.md` pushes the stronger long-term method idea: model the device as an operator rather than only as a nuisance label.

## Practical Development Guidance
- Every implementation task should state which research question it serves.
- Default engineering direction should preserve modular boundaries for:
  - dataset adapters
  - preprocessing
  - channel mapping
  - protocol splitting
  - baseline models
  - device-aware methods
  - evaluation and reporting
- Use lightweight, locally runnable defaults because the planned compute environment is local and resource constrained.

## Default Reading Rule For Future Tasks
- Start with this summary.
- Reopen the most relevant source documents before coding:
  - data task: prioritize `dataset-review/` and benchmark sections in `Document/phase1_*`
  - method task: prioritize `paper_review/`, `Document/phase1_core_innovations_algorithm_derivation.md`, and `Document/deep_algorithm_research_diode.md`
  - project-structure task: prioritize `Document/phase1_github_code_development_plan.md`
