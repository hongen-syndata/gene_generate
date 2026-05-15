from app.models.sequence import SequenceResult


def validate_sequence(seq: SequenceResult):
    """
    内部モデル SequenceResult の意味チェック。
    - FASTA の形式チェック
    - REF/ALT の配列長チェック
    - 配列が空でないこと
    """

    # --- FASTA ヘッダーのチェック ---
    if not seq.fasta_ref.startswith(">"):
        raise ValueError("REF FASTA header is missing")

    if not seq.fasta_alt.startswith(">"):
        raise ValueError("ALT FASTA header is missing")

    # --- FASTA 本体の抽出 ---
    ref_lines = seq.fasta_ref.split("\n")[1:]
    alt_lines = seq.fasta_alt.split("\n")[1:]

    ref_seq = "".join(ref_lines).strip()
    alt_seq = "".join(alt_lines).strip()

    # --- 空配列チェック ---
    if not ref_seq:
        raise ValueError("REF sequence is empty")

    if not alt_seq:
        raise ValueError("ALT sequence is empty")

    # --- 配列長チェック ---
    # substitution → REF と ALT の長さは同じ
    # deletion → ALT は REF より 1 塩基短い
    # insertion → MVP では未対応
    if len(ref_seq) == len(alt_seq):
        # substitution の可能性 → OK
        pass

    elif len(ref_seq) - len(alt_seq) == 1:
        # deletion の可能性 → OK
        pass

    else:
        raise ValueError(f"Sequence length mismatch: REF={len(ref_seq)}, ALT={len(alt_seq)}")

    return True
