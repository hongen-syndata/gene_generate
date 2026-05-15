from app.schemas.panel import GeneInfo as SGene, Panel, VariantInfo as SVariant
from app.services.normalize_panel import normalize_panel


def test_normalize_panel_basic():
    panel = Panel(
        disease="Cancer",
        generated_at="2025-01-01",
        genes=[
            SGene(
                gene="BRCA1",
                transcript="NM_007294",
                variants=[
                    SVariant(
                        cDNA="c.123A>T",
                        protein="p.Lys41Asn",
                        type="substitution",
                        significance="pathogenic",
                        explanation="test",
                    )
                ],
            )
        ],
    )

    genes, variants = normalize_panel(panel)

    # Gene の確認
    assert len(genes) == 1
    assert genes[0].name == "BRCA1"
    assert genes[0].transcript == "NM_007294"

    # Variant の確認
    assert len(variants) == 1
    v = variants[0]
    assert v.gene == "BRCA1"
    assert v.cDNA == "c.123A>T"
    assert v.type == "substitution"
