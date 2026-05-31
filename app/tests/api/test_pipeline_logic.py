from unittest.mock import MagicMock

from app.api.pipeline import run_pipeline_api


def test_run_pipeline_api(mocker):
    mock_sequences = [MagicMock(fasta_alt="ALT1", fasta_ref="REF1")]

    mocker.patch("app.api.pipeline.run_pipeline", return_value=mock_sequences)

    result = run_pipeline_api("HFE")

    assert result["count"] == 1
    assert result["first_alt"] == "ALT1"
    assert result["first_ref"] == "REF1"
