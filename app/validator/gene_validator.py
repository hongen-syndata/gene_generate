from app.models.gene import Gene


def validate_gene(gene: Gene):
    # Gene名のチェック
    if not gene.name or not gene.name.strip():
        raise ValueError("Gene name is empty")

    # Transcript の形式チェック（任意）
    if gene.transcript:
        if not gene.transcript.startswith("NM_"):
            raise ValueError(f"Invalid transcript format: {gene.transcript}")

    # Gene symbol の簡易チェック
    if not gene.name.replace("-", "").isalnum():
        raise ValueError(f"Invalid gene symbol: {gene.name}")

    return True
