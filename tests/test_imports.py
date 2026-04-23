from io import StringIO
from contextlib import redirect_stdout

from bci_trans_eeg import __version__
from bci_trans_eeg.cli import main
from bci_trans_eeg.data.registry import PHASE1_MI_DATASETS
from bci_trans_eeg.protocols.definitions import BenchmarkProtocol


def test_package_version_present() -> None:
    assert __version__ == "0.1.0"


def test_phase1_dataset_registry_not_empty() -> None:
    assert PHASE1_MI_DATASETS


def test_protocol_definition_shape() -> None:
    protocol = BenchmarkProtocol(
        name="zero_shot_lodo",
        source_datasets=("eegmmidb", "lee2019_mi"),
        target_dataset="cho2017",
        calibration_trials_per_class=0,
        notes="Smoke test for protocol scaffolding.",
    )
    assert protocol.target_dataset == "cho2017"


def test_cli_smoke_output() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["--smoke"])
    output = buffer.getvalue()
    assert exit_code == 0
    assert "datasets=4" in output
