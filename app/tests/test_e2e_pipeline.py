from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.repository import save_all
from app.schemas.panel import GeneInfo, Panel, VariantInfo
from app.services.generate_sequence import generate_sequence
from app.services.generate_snp import generate_snp
from app.services.normalize_panel import normalize_panel
from app.validation.validate_panel import validate_panel
from app.validator.sequence_validator import validate_sequence
from app.validator.snp_validator import validate_snp
from app.validator.variant_validator import validate_variant


def test_e2e_run_pipeline(mocker):
    # -----------------------------
    # ① メモリDBセットアップ
    # -----------------------------
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    # -----------------------------
    # ② 外部 JSON（schemas.Panel）
    # -----------------------------
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(
                gene="TP53",
                transcript="NM_000546.5",
                variants=[
                    VariantInfo(
                        cDNA="c.215C>G",
                        protein="p.Arg72Gly",
                        type="missense",
                        significance="Pathogenic",
                        explanation="TP53変異は腫瘍抑制機能を損なう",
                    )
                ],
            )
        ],
    )

    # -----------------------------
    # ③ validate_panel（外部 JSON）
    # -----------------------------
    validate_panel(panel)

    # -----------------------------
    # ④ normalize_panel（内部モデル化）
    # -----------------------------
    genes, variants = normalize_panel(panel)

    # -----------------------------
    # ⑤ validate_variant（内部 Variant）
    # -----------------------------
    for v in variants:
        validate_variant(v)

    # -----------------------------
    # ⑥ generate_snp（lookup_chromosome をモック）
    # -----------------------------
    mocker.patch("app.services.generate_snp.lookup_chromosome", return_value="17")
    snps = generate_snp(variants)

    # -----------------------------
    # ⑦ validate_snp
    # -----------------------------
    for snp in snps:
        validate_snp(snp)

    # -----------------------------
    # ⑧ generate_sequence（LLM をモック）
    # -----------------------------
    mocker.patch("app.services.generate_sequence.call_llm", return_value="A" * 300)
    sequences = [generate_sequence(snp) for snp in snps]

    # -----------------------------
    # ⑨ validate_sequence
    # -----------------------------
    for seq in sequences:
        validate_sequence(seq)

    # -----------------------------
    # ⑩ save_all（DB 保存）
    # -----------------------------
    panel_id = save_all(session, panel, genes, variants, snps, sequences)

    # -----------------------------
    # ⑪ DB 検証
    # -----------------------------
    # Panel
    panel_rows = session.execute(text("SELECT * FROM panel")).fetchall()
    assert len(panel_rows) == 1
    assert panel_rows[0].id == panel_id

    # Gene
    gene_rows = session.execute(text("SELECT * FROM gene")).fetchall()
    assert len(gene_rows) == 1
    assert gene_rows[0].name == "TP53"

    # Variant
    variant_rows = session.execute(text("SELECT * FROM variant")).fetchall()
    assert len(variant_rows) == 1
    assert variant_rows[0].cDNA == "c.215C>G"

    # SNP
    snp_rows = session.execute(text("SELECT * FROM snp")).fetchall()
    assert len(snp_rows) == 1
    assert snp_rows[0].pos == 215
    assert snp_rows[0].ref == "C"
    assert snp_rows[0].alt == "G"

    # Sequence
    seq_rows = session.execute(text("SELECT * FROM sequence")).fetchall()
    assert len(seq_rows) == 1
    assert ">TP53_REF" in seq_rows[0].ref_sequence
    assert ">TP53_ALT" in seq_rows[0].alt_sequence
