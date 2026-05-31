# tests/test_snp.py


from app.models.snp import SNP
from app.schemas.panel import GeneInfo, Panel, VariantInfo
from app.services.generate_snp import (
    generate_snp,
    lookup_chromosome,
    parse_cdna,
    parse_del,
    parse_snv,
)
from app.services.normalize_panel import normalize_panel


# -----------------------------
# 正常系：一致する gene がある
# -----------------------------
def test_lookup_chromosome_found(mocker):
    # モック CSV データ
    csv_content = "gene,chromosome\nBRCA1,17\nTP53,17\n"

    # open() をモック
    mocker.patch("builtins.open", mocker.mock_open(read_data=csv_content))

    # 実行
    result = lookup_chromosome("brca1")  # 小文字でも OK

    # 検証
    assert result == "17"


# -----------------------------
# 正常系：一致しない gene の場合 None
# -----------------------------
def test_lookup_chromosome_not_found(mocker):
    csv_content = "gene,chromosome\nBRCA1,17\n"

    mocker.patch("builtins.open", mocker.mock_open(read_data=csv_content))

    result = lookup_chromosome("TP53")

    assert result is None


# -----------------------------
# gene の前後に空白があっても一致する
# -----------------------------
def test_lookup_chromosome_strip_and_upper(mocker):
    csv_content = "gene,chromosome\nBRCA1,17\n"

    mocker.patch("builtins.open", mocker.mock_open(read_data=csv_content))

    result = lookup_chromosome("  brca1  ")

    assert result == "17"


# -----------------------------
# parse_snv のテスト
# -----------------------------
def test_parse_snv():
    cdna = "c.123A>T"
    result = parse_snv(cdna)

    assert result["pos"] == 123
    assert result["ref"] == "A"
    assert result["alt"] == "T"
    assert result["type"] == "substitution"


# -----------------------------
# parse_del のテスト
# -----------------------------
def test_parse_del():
    cdna = "c.456delG"
    result = parse_del(cdna)

    assert result["pos"] == 456
    assert result["ref"] == "G"
    assert result["alt"] == "-"
    assert result["type"] == "deletion"


# -----------------------------
# parse_cdna の unknown パターン
# -----------------------------
def test_parse_cdna_unknown():
    cdna = "c.???"
    result = parse_cdna(cdna)

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
                        type="missense",  # ★ normalize_panel が内部で扱う
                        significance="Pathogenic",
                        explanation="test explanation",
                    )
                ],
            )
        ],
    )

    # ★ normalize_panel を必ず通す
    genes, variants = normalize_panel(panel)

    # ★ lookup_chromosome をモック
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
    assert snp.type == "substitution"  # ★ cDNA から決まる
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
                        type="frameshift",
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

    snps = generate_snp(variants)

    assert len(snps) == 2

    snp1, snp2 = snps

    # 1つ目（substitution）
    assert snp1.pos == 100
    assert snp1.ref == "A"
    assert snp1.alt == "T"
    assert snp1.type == "substitution"

    # 2つ目（deletion）
    assert snp2.pos == 200
    assert snp2.ref == "G"
    assert snp2.alt == "-"
    assert snp2.type == "deletion"
