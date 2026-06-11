from app.db.session import get_session
from app.pipeline import run_pipeline  # ← 後で移動する
from app.services.result_builder import render_formatted


def run_pipeline_api(disease: str):
    with get_session() as session:
        result = run_pipeline(disease, session)
        return {
            "disease": result.disease,
            "count": len(result.results),
            "results": [r.model_dump() for r in result.results],
            "formatted": render_formatted(result),
        }
