from app.db.session import get_session
from app.pipeline import run_pipeline  # ← 後で移動する


def run_pipeline_api(disease: str):
    with get_session() as session:
        sequences = run_pipeline(disease, session)
        return {
            "count": len(sequences),
            "first_alt": sequences[0].fasta_alt,
            "first_ref": sequences[0].fasta_ref,
        }
