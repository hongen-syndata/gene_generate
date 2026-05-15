from app.models.gene import Gene
from app.models.variant import Variant
from app.schemas.panel import Panel  # PanelDetailed
from app.validator.gene_validator import validate_gene
from app.validator.variant_validator import validate_variant


def normalize_panel(panel: Panel) -> tuple[list[Gene], list[Variant]]:
    """
    PanelDetailed(JSON) → 内部モデル(Gene[], Variant[]) に変換する。
    変換後に内部バリデーションも実行する。
    """

    genes: list[Gene] = []
    variants: list[Variant] = []

    for g in panel.genes:
        # Gene の正規化
        gene = Gene(
            name=g.gene,  # LLM JSON のフィールド名に合わせる
            transcript=g.transcript,
        )
        validate_gene(gene)
        genes.append(gene)

        # Variant の正規化
        for v in g.variants:
            variant = Variant(
                gene=g.gene,
                cDNA=v.cDNA,
                protein=v.protein,
                type=v.type,
                significance=v.significance,
                explanation=v.explanation,
            )
            validate_variant(variant)
            variants.append(variant)

    return genes, variants
