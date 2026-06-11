from fastapi.testclient import TestClient

from app.main import app
from app.schemas.result import GeneResult, PipelineResult

client = TestClient(app)


def test_pipeline_endpoint(mocker):
    # --- run_pipeline の戻り値（PipelineResult）を作る ---
    mock_result = PipelineResult(
        disease="Cancer",
        results=[
            GeneResult(
                gene="TP53",
                significance="Pathogenic",
                explanation="TP53変異は腫瘍抑制機能を損なう",
                sequence="ACGT",
            ),
            GeneResult(
                gene="BRCA1",
                significance="Likely pathogenic",
                explanation="DNA修復機能の低下",
                sequence="TTGG",
            ),
        ],
    )

    # --- run_pipeline_api が内部で呼ぶ run_pipeline をモック ---
    mocker.patch("app.api.pipeline.run_pipeline", return_value=mock_result)

    # --- API 呼び出し ---
    response = client.post("/pipeline/run", json={"disease": "Cancer"})

    # --- 検証 ---
    assert response.status_code == 200
    data = response.json()

    assert data["disease"] == "Cancer"
    assert data["count"] == 2
    assert data["results"][0]["gene"] == "TP53"
    assert data["results"][0]["significance"] == "Pathogenic"
    assert data["results"][0]["sequence"] == "ACGT"

    # 整形テキストに疾患名・遺伝子名・臨床的意義・塩基配列が含まれる
    formatted = data["formatted"]
    assert "疾患名:Cancer" in formatted
    assert "遺伝子名1:TP53" in formatted
    assert "臨床的意義:Pathogenic / TP53変異は腫瘍抑制機能を損なう" in formatted
    assert "塩基配列:ACGT" in formatted
    assert "遺伝子名2:BRCA1" in formatted
