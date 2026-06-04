from app.models.snp import SNP


def validate_snp(snp: SNP):
    # gene
    if not snp.gene or not snp.gene.strip():
        raise ValueError("SNP.gene is empty")

    # chromosome（None の場合は許容：lookup_chromosome が見つけられないケース）
    if snp.chrom is not None:
        if not snp.chrom.replace("chr", "").isalnum():
            raise ValueError(f"Invalid chromosome format: {snp.chrom}")

    # pos
    if snp.pos is None or snp.pos <= 0:
        raise ValueError(f"Invalid SNP position: {snp.pos}")

    # ref / alt
    valid_alleles = {"A", "T", "C", "G", "-"}
    if snp.ref not in valid_alleles:
        raise ValueError(f"Invalid ref allele: {snp.ref}")

    if snp.alt not in valid_alleles:
        raise ValueError(f"Invalid alt allele: {snp.alt}")

    # type（generate_snp が付与したものと整合しているか）
    if snp.type not in ["substitution", "deletion", "unknown"]:
        raise ValueError(f"Invalid SNP type: {snp.type}")

    # explanation は空でも許容（LLM が生成しないケースがあるため）

    return True
