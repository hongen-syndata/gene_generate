import pytest

from app.models.gene import Gene
from app.validator.gene_validator import validate_gene


def test_validate_gene_ok():
    gene = Gene(name="BRCA1", transcript="NM_007294")
    assert validate_gene(gene) is True


def test_validate_gene_empty_name():
    gene = Gene(name="", transcript="NM_007294")
    with pytest.raises(ValueError):
        validate_gene(gene)


def test_validate_gene_invalid_transcript():
    gene = Gene(name="BRCA1", transcript="XYZ_123")
    with pytest.raises(ValueError):
        validate_gene(gene)
