from app.api.pipeline import run_pipeline_api
from app.schemas.result import GeneResult, PipelineResult


def test_run_pipeline_api(mocker):
    mock_result = PipelineResult(
        disease="Cancer",
        results=[
            GeneResult(
                gene="TP53",
                significance="Pathogenic",
                explanation="TP53変異は腫瘍抑制機能を損なう",
                sequence="ACGT",
            )
        ],
    )

    mocker.patch("app.api.pipeline.run_pipeline", return_value=mock_result)

    result = run_pipeline_api("Cancer")

    assert result["disease"] == "Cancer"
    assert result["count"] == 1
    assert result["results"][0]["gene"] == "TP53"
    assert result["results"][0]["sequence"] == "ACGT"
    assert "疾患名:Cancer" in result["formatted"]
