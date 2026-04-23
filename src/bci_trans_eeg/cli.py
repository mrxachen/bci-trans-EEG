"""Minimal CLI entrypoint for repository scaffolding."""

from __future__ import annotations

import argparse
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bci-trans-eeg",
        description="Phase I utilities for the cross-device EEG benchmark codebase.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the package version and exit.",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a minimal scaffold smoke check and exit.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        from bci_trans_eeg import __version__

        print(__version__)
        return 0

    if args.smoke:
        from bci_trans_eeg import __version__
        from bci_trans_eeg.data.registry import PHASE1_MI_DATASETS

        print(f"bci-trans-eeg {__version__}")
        print(f"datasets={len(PHASE1_MI_DATASETS)}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
