from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.repository import save_all
from app.models.gene import Gene
from app.models.sequence import SequenceResult
from app.models.snp import SNP
from app.models.variant import Variant
from app.schemas.panel import Panel


def test_save_all():
    # メモリDB
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()

    # 外部 JSON
    panel = Panel(disease="Cancer", generated_at="2025-01-01", genes=[])

    # 内部モデル
    genes = [Gene(name="BRCA1", transcript="NM_007294")]
    variants = [
        Variant(
            gene="BRCA1",
            cDNA="c.123A>T",
            protein=None,
            type="substitution",
            significance=None,
            explanation=None,
        )
    ]
    snps = [
        SNP(
            gene="BRCA1",
            ref="A",
            alt="T",
            pos=123,
            chrom="17",
            type="substitution",
        )
    ]
    sequences = [SequenceResult(fasta_ref=">ref\nAAA", fasta_alt=">alt\nATA")]

    panel_id = save_all(session, panel, genes, variants, snps, sequences)

    # Panel が保存されているか
    assert panel_id == 1
    from sqlalchemy import text

    # Gene が保存されているか
    gene_rows = session.execute(text("SELECT * FROM gene")).fetchall()
    assert len(gene_rows) == 1
    assert gene_rows[0].name == "BRCA1"

    # Variant が保存されているか
    variant_rows = session.execute(text("SELECT * FROM variant")).fetchall()
    assert len(variant_rows) == 1
    assert variant_rows[0].cDNA == "c.123A>T"

    # SNP が保存されているか
    snp_rows = session.execute(text("SELECT * FROM snp")).fetchall()
    assert len(snp_rows) == 1
    assert snp_rows[0].ref == "A"

    # Sequence が保存されているか
    seq_rows = session.execute(text("SELECT * FROM sequence")).fetchall()
    assert len(seq_rows) == 1
    assert seq_rows[0].alt_sequence.startswith(">alt")
