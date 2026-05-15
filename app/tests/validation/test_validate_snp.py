import pytest

from app.schemas.snp import SNP
from app.validation.validate_snp import validate_snp


# --- 正常系 ---
def test_validate_snp_substitution_ok():
    snp = SNP(
        gene="BRCA1",
        pos=100,
        ref="A",
        alt="G",
        type="substitution"
    )
    validate_snp(snp)  # 例外が出なければ OK


def test_validate_snp_deletion_ok():
    snp = SNP(
        gene="TP53",
        pos=50,
        ref="C",
        alt="-",
        type="deletion"
    )
    validate_snp(snp)


# --- ref/alt が不正 ---
@pytest.mark.parametrize("ref,alt", [
    ("X", "A"),
    ("A", "X"),
    ("N", "T"),
    ("A", "AA"),  # substitution では長さ不正
])
def test_validate_snp_invalid_bases(ref, alt):
    snp = SNP(
        gene="BRCA1",
        pos=10,
        ref=ref,
        alt=alt,
        type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


# --- type が不正 ---
def test_validate_snp_invalid_type():
    snp = SNP(
        gene="BRCA1",
        pos=10,
        ref="A",
        alt="G",
        type="unknown"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


# --- substitution の ref/alt が不正 ---
@pytest.mark.parametrize("ref,alt", [
    ("-", "A"),   # "-" を含む
    ("A", "-"),
    ("AA", "G"),  # 2 塩基
    ("A", "GG"),
])
def test_validate_snp_substitution_invalid(ref, alt):
    snp = SNP(
        gene="BRCA1",
        pos=10,
        ref=ref,
        alt=alt,
        type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


# --- deletion の alt が "-" でない ---
def test_validate_snp_deletion_invalid_alt():
    snp = SNP(
        gene="BRCA1",
        pos=10,
        ref="A",
        alt="G",
        type="deletion"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


# --- pos が 1 未満 ---
def test_validate_snp_invalid_pos():
    snp = SNP(
        gene="BRCA1",
        pos=0,
        ref="A",
        alt="G",
        type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


# --- gene が空文字 ---
def test_validate_snp_empty_gene():
    snp = SNP(
        gene="",
        pos=10,
        ref="A",
        alt="G",
        type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)
