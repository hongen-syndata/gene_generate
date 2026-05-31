from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pipeline_endpoint(mocker):
    # --- モックの戻り値を作る ---
    mock_sequences = [
        MagicMock(fasta_alt="ALT1", fasta_ref="REF1"),
        MagicMock(fasta_alt="ALT2", fasta_ref="REF2"),
    ]

    # --- run_pipeline_api が内部で呼ぶ run_pipeline をモック ---
    mocker.patch("app.api.pipeline.run_pipeline", return_value=mock_sequences)

    # --- API 呼び出し ---
    response = client.post("/pipeline/run", json={"disease": "HFE"})

    # --- 検証 ---
    assert response.status_code == 200
    data = response.json()

    assert data["count"] == 2
    assert data["first_alt"] == "ALT1"
    assert data["first_ref"] == "REF1"
