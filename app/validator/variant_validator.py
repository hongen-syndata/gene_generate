import re

from app.models.variant import Variant

CDNA_SUB_PATTERN = re.compile(r"^c\.(\d+)([ACGT])>([ACGT])$")
CDNA_DEL_PATTERN = re.compile(r"^c\.(\d+)del([ACGT])$")


def validate_variant(variant: Variant):
    # gene が空
    if not variant.gene or not variant.gene.strip():
        raise ValueError("Variant.gene is empty")

    cdna = variant.cDNA.strip()

    # cDNA の形式チェック
    if not (CDNA_SUB_PATTERN.match(cdna) or CDNA_DEL_PATTERN.match(cdna)):
        raise ValueError(f"Invalid cDNA format: {variant.cDNA}")

    # type はタンパク質レベルの分類として妥当かだけチェック
    allowed_types = {"missense", "nonsense", "frameshift", "splice", "inframe", "unknown"}
    if variant.type and variant.type not in allowed_types:
        raise ValueError(f"Invalid variant.type: {variant.type}")

    # cDNA の分類とは比較しない（重要）
    return True
