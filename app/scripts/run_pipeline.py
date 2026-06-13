from app.db.session import get_session
from app.pipeline import run_pipeline  # ← 後で移動する
from app.services.result_builder import render_formatted

if __name__ == "__main__":
    from app.db.session import get_session

    with get_session() as session:
        result = run_pipeline("HFE", session)
        print(render_formatted(result))
