import pytest

from app.models.variant import Variant
from app.validator.variant_validator import validate_variant


def test_validate_variant_substitution_ok():
    v = Variant(
        gene="BRCA1",
        cDNA="c.123A>T",
        protein="p.Lys41Asn",
        type="missense",
        significance="pathogenic",
        explanation="test",
    )
    assert validate_variant(v) is True


def test_validate_variant_deletion_ok():
    v = Variant(
        gene="BRCA1",
        cDNA="c.123delA",
        protein=None,
        type="nonsense",
        significance=None,
        explanation=None,
    )
    assert validate_variant(v) is True


def test_validate_variant_invalid_cdna():
    v = Variant(
        gene="BRCA1", cDNA="invalid", protein=None, type=None, significance=None, explanation=None
    )
    with pytest.raises(ValueError):
        validate_variant(v)


def test_validate_variant_type_mismatch():
    v = Variant(
        gene="BRCA1",
        cDNA="c.123A>T",
        protein=None,
        type="deletion",  # 本来は substitution
        significance=None,
        explanation=None,
    )
    with pytest.raises(ValueError):
        validate_variant(v)
