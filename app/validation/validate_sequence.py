def validate_sequence(fasta: str) -> None:
    """
    Validate the biological correctness and formatting of a FASTA sequence.
    """

    # --- FASTA の基本構造チェック ---
    lines = fasta.strip().split("\n")
    if len(lines) < 2:
        raise ValueError("FASTA must contain a header and a sequence line")

    header, seq = lines[0], "".join(lines[1:])

    if not header.startswith(">"):
        raise ValueError("FASTA header must start with '>'")

    if not seq:
        raise ValueError("FASTA sequence is empty")

    # --- 塩基チェック ---
    valid_bases = {"A", "T", "C", "G"}
    if any(base not in valid_bases for base in seq):
        raise ValueError("Sequence contains invalid bases")

    # --- 長さチェック ---
    if len(seq) < 50 or len(seq) > 200:
        raise ValueError(f"Sequence length out of range: {len(seq)}")

    # --- GC% チェック ---
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    if gc < 0.2 or gc > 0.8:
        raise ValueError(f"GC content out of range: {gc:.2f}")
