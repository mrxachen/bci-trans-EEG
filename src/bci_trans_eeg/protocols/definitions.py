"""Protocol structures for benchmark splits and calibration settings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkProtocol:
    name: str
    source_datasets: tuple[str, ...]
    target_dataset: str
    calibration_trials_per_class: int
    notes: str
