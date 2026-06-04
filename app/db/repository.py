from datetime import datetime

from app.db.model.gene import Gene
from app.db.model.panel import Panel
from app.db.model.sequence import Sequence
from app.db.model.snp import SNP
from app.db.model.variant import Variant
from app.services.generate_snp import parse_cdna  # ★ Variant の cDNA を解析するため


def save_all(session, panel_data, genes, variants, snps, sequences):
    """
    panel_data: schemas.PanelDetailed（外部モデル）
    genes: List[models.Gene]（内部モデル）
    variants: List[models.Variant]（内部モデル）
    snps: List[models.SNP]（内部モデル）
    sequences: List[models.SequenceResult]（内部モデル）
    """

    # ① Panel
    panel_row = Panel(disease=panel_data.disease, created_at=datetime.now())
    session.add(panel_row)
    session.flush()

    # ② Gene
    gene_map = {}
    for g in genes:
        gene_row = Gene(panel_id=panel_row.id, name=g.name, transcript=g.transcript)
        session.add(gene_row)
        session.flush()
        gene_map[g.name] = gene_row.id

    # ③ Variant（pos/ref/alt で引けるようにマップを作る）
    variant_map = {}  # key = (gene, pos, ref, alt)

    for v in variants:
        variant_row = Variant(
            gene_id=gene_map[v.gene],
            cDNA=v.cDNA,
            protein=v.protein,
            type=v.type,
            significance=v.significance,
            explanation=v.explanation,
        )
        session.add(variant_row)
        session.flush()

        # ★ cDNA を解析して pos/ref/alt を取得
        parsed = parse_cdna(v.cDNA)
        key = (v.gene, parsed["pos"], parsed["ref"], parsed["alt"])
        variant_map[key] = variant_row.id

    # ④ SNP（複数）
    snp_rows = []
    for snp in snps:
        # ★ SNP は cDNA を持たないので、pos/ref/alt で Variant を特定する
        key = (snp.gene, snp.pos, snp.ref, snp.alt)
        variant_id = variant_map[key]

        snp_row = SNP(
            variant_id=variant_id,
            ref=snp.ref,
            alt=snp.alt,
            pos=snp.pos,
        )
        session.add(snp_row)
        session.flush()
        snp_rows.append(snp_row)

    # ⑤ Sequence（複数）
    for snp_row, seq in zip(snp_rows, sequences, strict=True):
        seq_row = Sequence(
            snp_id=snp_row.id,
            ref_sequence=seq.fasta_ref,
            alt_sequence=seq.fasta_alt,
        )
        session.add(seq_row)

    # ⑥ commit
    session.commit()

    return panel_row.id
