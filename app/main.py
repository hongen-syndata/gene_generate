from sqlalchemy.orm import Session

from app.db.base import Base, engine
from app.db.repository import save_all
from app.schemas.panel import Panel
from app.services.generate_panel import generate_panel
from app.services.generate_sequence import generate_sequence
from app.services.generate_snp import generate_snp
from app.services.normalize_panel import normalize_panel
from app.validation.validate_panel import validate_panel
from app.validator.gene_validator import validate_gene
from app.validator.sequence_validator import validate_sequence
from app.validator.snp_validator import validate_snp
from app.validator.variant_validator import validate_variant

# DB 初期化（テーブル作成）
Base.metadata.create_all(bind=engine)
# ★★★★★★★★★★★★★★★★


def run_pipeline(disease: str, session: Session) -> int:
    """
    Full pipeline:
    disease → panel(JSON) → internal models → SNP → sequence → DB保存
    Returns: panel_id
    """

    # ① パネル生成（LLM）
    print("[1] generate_panel 開始")
    panel_json: Panel = generate_panel(disease)

    # ② 外部JSONの構造チェック
    validate_panel(panel_json)

    # ③ 内部モデルへ正規化
    print("[2] normalize_panel 開始")
    genes, variants = normalize_panel(panel_json)

    # ④ Gene / Variant の内部バリデーション
    for g in genes:
        validate_gene(g)

    print(f"[3] Variant 数: {len(variants)} 件 → validate_variant 実行中...")
    for v in variants:
        validate_variant(v)

    # ⑤ SNP 生成（内部モデル）
    print("[4] generate_snp 開始")
    snps = generate_snp(variants)

    # ⑥ SNP の内部バリデーション
    print(f"[5] SNP 数: {len(snps)} 件 → validate_snp 実行中...")
    for snp in snps:
        validate_snp(snp)

    # ⑦ Sequence 生成（内部モデル）
    print("[6] generate_sequence 開始")
    sequences = [generate_sequence(snp) for snp in snps]

    # ⑧ Sequence の内部バリデーション
    print("[7] validate_sequence 開始")
    for seq in sequences:
        validate_sequence(seq)

    # ⑨ DB 保存（Panel / Gene / Variant / SNP / Sequence）
    print("[8] DB 保存中...")
    save_all(
        session=session,
        panel_data=panel_json,
        genes=genes,
        variants=variants,
        snps=snps,
        sequences=sequences,
    )

    print("完了しました。")
    return sequences


if __name__ == "__main__":
    from app.db.session import get_session

    with get_session() as session:
        sequences = run_pipeline("HFE", session)
        print(sequences[0].fasta_alt)
        print(sequences[0].fasta_ref)
