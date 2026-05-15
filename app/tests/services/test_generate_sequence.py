# tests/test_sequence.py
import pytest

from app.models.sequence import SequenceResult
from app.models.snp import SNP
from app.services.generate_sequence import (
    apply_variant,
    generate_sequence,
    handle_deletion,
    handle_substitution,
    to_fasta,
)


# -----------------------------
# handle_substitution のテスト
# -----------------------------
def test_handle_substitution():
    # Arrange
    ref_seq = "ATCG"
    pos = 2
    ref = "T"
    alt = "G"

    # Act
    result = handle_substitution(ref_seq, pos, ref, alt)

    # Assert
    assert result == "AGCG"


# -----------------------------
# handle_deletion のテスト
# -----------------------------
def test_handle_deletion():
    # Arrange
    ref_seq = "ATCG"
    pos = 3
    ref = "C"
    alt = "-"

    # Act
    result = handle_deletion(ref_seq, pos, ref, alt)

    # Assert
    assert result == "ATG"


# -----------------------------
# apply_variant の正常系
# -----------------------------
def test_apply_variant_substitution():
    # Arrange
    ref_seq = "AAAAA"

    # Act
    result = apply_variant(ref_seq, pos=3, ref="A", alt="T")

    # Assert
    assert result == "AATAA"


def test_apply_variant_deletion():
    # Arrange
    ref_seq = "ACTGA"

    # Act
    result = apply_variant(ref_seq, pos=2, ref="C", alt="-")

    # Assert
    assert result == "ATGA"


# -----------------------------
# apply_variant の異常系
# -----------------------------
def test_apply_variant_unsupported():
    # Arrange
    ref_seq = "AAAAA"

    # Act & Assert
    with pytest.raises(ValueError):
        apply_variant(ref_seq, pos=3, ref="A", alt="XYZ")  # 不正 ALT


# -----------------------------
# to_fasta のテスト
# -----------------------------
def test_to_fasta():
    # Arrange
    header = "TEST"
    sequence = "ATCGATCG"
    line_width = 4

    # Act
    result = to_fasta(header, sequence, line_width)

    # Assert
    assert result == ">TEST\nATCG\nATCG"


# -----------------------------
# generate_sequence のテスト（LLM モック）
# -----------------------------
def test_generate_sequence(mocker):
    # Arrange
    snp = SNP(
        gene="BRCA1",
        chrom="17",
        pos=3,
        ref="A",
        alt="T",
        type="substitution",
    )

    # LLM の返り値をモック（100bp でなくても OK）
    mocker.patch(
        "app.services.generate_sequence.call_llm",
        return_value="AAAATGCG",  # pos=3 の A を T に変える
    )

    # Act
    result = generate_sequence(snp)

    # Assert
    assert isinstance(result, SequenceResult)

    # REF FASTA
    assert result.fasta_ref.startswith(">BRCA1_REF")
    assert "AAAATGCG" in result.fasta_ref

    # ALT FASTA
    assert result.fasta_alt.startswith(">BRCA1_ALT")
    assert "AATATGCG" in result.fasta_alt  # pos=3 の A が T に置換されている
