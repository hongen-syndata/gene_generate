from app.db.session import get_session
from app.pipeline import run_pipeline  # ← 後で移動する

if __name__ == "__main__":
    from app.db.session import get_session

    with get_session() as session:
        sequences = run_pipeline("HFE", session)
        print(sequences[0].fasta_alt)
        print(sequences[0].fasta_ref)
