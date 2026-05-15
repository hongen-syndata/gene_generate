import pytest

from app.models.sequence import SequenceResult
from app.validator.sequence_validator import validate_sequence


def test_validate_sequence_ok():
    seq = SequenceResult(
        fasta_ref=">ref\nAAA",
        fasta_alt=">alt\nATA"
    )
    assert validate_sequence(seq) is True


def test_validate_sequence_missing_header():
    seq = SequenceResult(
        fasta_ref="ref\nAAA",
        fasta_alt=">alt\nATA"
    )
    with pytest.raises(ValueError):
        validate_sequence(seq)


def test_validate_sequence_empty_body():
    seq = SequenceResult(
        fasta_ref=">ref\n",
        fasta_alt=">alt\nATA"
    )
    with pytest.raises(ValueError):
        validate_sequence(seq)
