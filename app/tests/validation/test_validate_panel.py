import pytest

from app.schemas.panel import GeneInfo, Panel
from app.validation.validate_panel import validate_panel


# --- 正常系 ---
def test_validate_panel_ok():
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(gene="BRCA1", transcript="NM_007294", variants=[]),
            GeneInfo(gene="TP53", transcript="NM_000546", variants=[]),
            GeneInfo(gene="EGFR", transcript="NM_005228", variants=[]),
        ],
    )
    validate_panel(panel)


# --- genes が空 ---
def test_validate_panel_empty_genes():
    panel = Panel(disease="Cancer", generated_at="2025-01-01", genes=[])
    with pytest.raises(ValueError):
        validate_panel(panel)


# --- gene 名が空文字 ---
def test_validate_panel_empty_gene_name():
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(gene="BRCA1", transcript="NM_007294", variants=[]),
            GeneInfo(gene="", transcript="NM_000546", variants=[]),
        ],
    )
    with pytest.raises(ValueError):
        validate_panel(panel)


# --- gene 名に不正文字 ---
@pytest.mark.parametrize("bad_gene", ["BRCA1?", "TP53!", "EGFR-", "BRCA 1"])
def test_validate_panel_invalid_characters(bad_gene):
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(gene="BRCA1", transcript="NM_007294", variants=[]),
            GeneInfo(gene=bad_gene, transcript="NM_000546", variants=[]),
        ],
    )
    with pytest.raises(ValueError):
        validate_panel(panel)


# --- 重複 gene ---
def test_validate_panel_duplicate_genes():
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(gene="BRCA1", transcript="NM_007294", variants=[]),
            GeneInfo(gene="BRCA1", transcript="NM_007294", variants=[]),
        ],
    )
    with pytest.raises(ValueError):
        validate_panel(panel)


# --- gene 数が多すぎる ---
def test_validate_panel_too_many_genes():
    many_genes = [GeneInfo(gene=f"GENE{i}", transcript="NM_xxx", variants=[]) for i in range(60)]
    panel = Panel(disease="Cancer", generated_at="2025-01-01", genes=many_genes)
    with pytest.raises(ValueError):
        validate_panel(panel)
