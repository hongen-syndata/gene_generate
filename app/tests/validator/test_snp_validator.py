import pytest

from app.models.snp import SNP
from app.validator.snp_validator import validate_snp


def test_validate_snp_ok():
    snp = SNP(
        gene="BRCA1", cDNA="c.123A>T", ref="A", alt="T", pos=123, chrom="17", type="substitution"
    )
    assert validate_snp(snp) is True


def test_validate_snp_invalid_pos():
    snp = SNP(
        gene="BRCA1", cDNA="c.123A>T", ref="A", alt="T", pos=-1, chrom="17", type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)


def test_validate_snp_invalid_allele():
    snp = SNP(
        gene="BRCA1", cDNA="c.123A>T", ref="X", alt="T", pos=123, chrom="17", type="substitution"
    )
    with pytest.raises(ValueError):
        validate_snp(snp)
