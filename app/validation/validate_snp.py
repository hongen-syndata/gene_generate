# app/validation/validate_snp.py

from app.schemas.snp import SNP


def validate_snp(snp: SNP) -> None:
    """
    Validate biological correctness of SNP information.
    """
    # --- gene が空 ---
    if not snp.gene or not snp.gene.strip():
        raise ValueError("SNP.gene is empty")

    # --- 基本チェック ---
    valid_bases = {"A", "T", "C", "G", "-"}
    if snp.ref not in valid_bases:
        raise ValueError(f"Invalid ref base: {snp.ref}")

    if snp.alt not in valid_bases:
        raise ValueError(f"Invalid alt base: {snp.alt}")

    # --- type ごとのルール定義 ---
    # 今は substitution / deletion のみ対応
    type_rules = {
        "substitution": lambda ref, alt: (
            ref != "-" and alt != "-" and len(ref) == 1 and len(alt) == 1
        ),
        "deletion": lambda ref, alt: ref in {"A", "T", "C", "G"} and alt == "-",
        # "insertion": lambda ref, alt: (ref == "-" and alt in {"A","T","C","G"}),
    }

    if snp.type not in type_rules:
        raise ValueError(f"Unsupported variant type: {snp.type}")

    # --- type ごとの整合性チェック ---
    if not type_rules[snp.type](snp.ref, snp.alt):
        raise ValueError(
            f"ref/alt combination is invalid for type '{snp.type}' (ref={snp.ref}, alt={snp.alt})"
        )

    # --- pos チェック ---
    if snp.pos < 1:
        raise ValueError(f"Position must be >= 1, got {snp.pos}")
