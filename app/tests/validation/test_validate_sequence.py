import pytest

from app.validation.validate_sequence import validate_sequence


# --- 正常系 ---
def test_validate_sequence_ok():
    fasta = ">BRCA1_REF\n" + "ATCG" * 20  # 80bp
    validate_sequence(fasta)  # 例外が出なければ OK


# --- FASTA が1行しかない ---
def test_validate_sequence_single_line():
    fasta = ">BRCA1_REF"
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- ヘッダが '>' で始まらない ---
def test_validate_sequence_invalid_header():
    fasta = "BRCA1_REF\nATCGATCG"
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- 配列が空 ---
def test_validate_sequence_empty_sequence():
    fasta = ">BRCA1_REF\n"
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- 不正な塩基 ---
@pytest.mark.parametrize("bad_seq", [
    "ATCXATCG",   # X
    "ATNGATCG",   # N
    "ATC-ATCG",   # -
    "ATC1ATCG",   # 数字
])
def test_validate_sequence_invalid_bases(bad_seq):
    fasta = ">BRCA1_REF\n" + bad_seq
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- 長さが短すぎる ---
def test_validate_sequence_too_short():
    fasta = ">BRCA1_REF\n" + "A" * 10
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- 長さが長すぎる ---
def test_validate_sequence_too_long():
    fasta = ">BRCA1_REF\n" + "A" * 300
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- GC% が極端（0%） ---
def test_validate_sequence_gc_too_low():
    fasta = ">BRCA1_REF\n" + "A" * 100
    with pytest.raises(ValueError):
        validate_sequence(fasta)


# --- GC% が極端（100%） ---
def test_validate_sequence_gc_too_high():
    fasta = ">BRCA1_REF\n" + "G" * 100
    with pytest.raises(ValueError):
        validate_sequence(fasta)
