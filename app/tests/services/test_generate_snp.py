# tests/test_snp.py
from app.models.snp import SNP
from app.schemas.panel import GeneInfo, Panel, VariantInfo
from app.services.generate_snp import generate_snp, parse_cdna, parse_del, parse_snv
from app.services.normalize_panel import normalize_panel


# -----------------------------
# parse_snv のテスト
# -----------------------------
def test_parse_snv():
    # Arrange
    cdna = "c.123A>T"

    # Act
    result = parse_snv(cdna)

    # Assert
    assert result["pos"] == 123
    assert result["ref"] == "A"
    assert result["alt"] == "T"
    assert result["type"] == "substitution"


# -----------------------------
# parse_del のテスト
# -----------------------------
def test_parse_del():
    # Arrange
    cdna = "c.456delG"

    # Act
    result = parse_del(cdna)

    # Assert
    assert result["pos"] == 456
    assert result["ref"] == "G"
    assert result["alt"] == "-"
    assert result["type"] == "deletion"


# -----------------------------
# parse_cdna の unknown パターン
# -----------------------------
def test_parse_cdna_unknown():
    # Arrange
    cdna = "c.???"

    # Act
    result = parse_cdna(cdna)

    # Assert
    assert result["pos"] is None
    assert result["ref"] is None
    assert result["alt"] is None
    assert result["type"] == "unknown"


# -----------------------------
# generate_snp（単一 variant）
# -----------------------------
def test_generate_snp_single_variant(mocker):
    panel = Panel(
        disease="TestDisease",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(
                gene="BRCA1",
                transcript="NM_000000.0",
                variants=[
                    VariantInfo(
                        cDNA="c.123A>T",
                        protein="p.Lys41Asn",
                        type="missense",
                        significance="Pathogenic",
                        explanation="test explanation",
                    )
                ],
            )
        ],
    )

    # ★ normalize_panel を必ず通す
    genes, variants = normalize_panel(panel)

    # lookup_chromosome をモック
    mocker.patch("app.services.generate_snp.lookup_chromosome", return_value="17")

    # ★ generate_snp(panel) は絶対にダメ
    snps = generate_snp(variants)

    assert len(snps) == 1
    snp = snps[0]

    assert isinstance(snp, SNP)
    assert snp.gene == "BRCA1"
    assert snp.chrom == "17"
    assert snp.pos == 123
    assert snp.ref == "A"
    assert snp.alt == "T"
    assert snp.type == "substitution"
    assert snp.explanation == "test explanation"


# -----------------------------
# generate_snp（複数 variant）
# -----------------------------
def test_generate_snp_multiple_variants(mocker):
    panel = Panel(
        disease="TestDisease",
        generated_at="2025-01-01",
        genes=[
            GeneInfo(
                gene="TP53",
                transcript="NM_000000.1",
                variants=[
                    VariantInfo(
                        cDNA="c.100A>T",
                        protein="p.Lys34Asn",
                        type="missense",
                        significance="Likely pathogenic",
                        explanation="exp1",
                    ),
                    VariantInfo(
                        cDNA="c.200delG",
                        protein="p.Gly66fs",
                        type="missense",
                        significance="Pathogenic",
                        explanation="exp2",
                    ),
                ],
            )
        ],
    )

    # ★ normalize_panel を必ず通す
    genes, variants = normalize_panel(panel)

    mocker.patch("app.services.generate_snp.lookup_chromosome", return_value="17")

    # ★ generate_snp(panel) は絶対にダメ
    snps = generate_snp(variants)

    assert len(snps) == 2

    snp1, snp2 = snps

    assert snp1.pos == 100
    assert snp1.ref == "A"
    assert snp1.alt == "T"

    assert snp2.pos == 200
    assert snp2.ref == "G"
    assert snp2.alt == "-"
