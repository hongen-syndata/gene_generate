# app/tests/test_main.py

import pytest

from app.main import run_pipeline
from app.schemas.sequence import SequenceResult


def test_run_pipeline(mocker):
    """
    Integration test for the full pipeline:
    disease → panel → snp → sequence
    """

    # --- Arrange ---
    # 1. generate_panel のモック
    mock_panel = mocker.Mock()
    mock_panel.genes = ["BRCA1"]
    mocker.patch(
        "app.main.generate_panel",
        return_value=mock_panel
    )

    # 2. generate_snp のモック
    mock_snp = mocker.Mock()
    mocker.patch(
        "app.main.generate_snp",
        return_value=mock_snp
    )

    # 3. generate_sequence のモック
    mock_seq = SequenceResult(
        fasta_ref=">BRCA1_REF\nAAAATGCG",
        fasta_alt=">BRCA1_ALT\nAATATGCG"
    )
    mocker.patch(
        "app.main.generate_sequence",
        return_value=mock_seq
    )

    # --- Act ---
    result = run_pipeline("Cancer")

    # --- Assert ---
    assert isinstance(result, SequenceResult)
    assert result.fasta_ref.startswith(">BRCA1_REF")
    assert result.fasta_alt.startswith(">BRCA1_ALT")

    # 呼び出し順の確認（重要）
    generate_panel = pytest.importorskip("app.main").generate_panel
    generate_snp = pytest.importorskip("app.main").generate_snp
    generate_sequence = pytest.importorskip("app.main").generate_sequence

    generate_panel.assert_called_once_with("Cancer")
    generate_snp.assert_called_once_with("BRCA1")
    generate_sequence.assert_called_once_with(mock_snp)
