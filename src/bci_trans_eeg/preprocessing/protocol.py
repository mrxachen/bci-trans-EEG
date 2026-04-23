"""Preprocessing configuration types for benchmark runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PreprocessingSpec:
    bandpass_low_hz: float
    bandpass_high_hz: float
    target_sampling_rate_hz: int
    rereference: str
    normalization: str
