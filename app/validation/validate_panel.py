import re

from app.schemas.panel import Panel


def validate_panel(panel: Panel) -> None:
    # 1. genes が空でない
    if not panel.genes:
        raise ValueError("Panel contains no genes")

    # 正規表現（A-Z, 0-9, _ のみ許可）
    pattern = re.compile(r"^[A-Za-z0-9_]+$")

    seen = set()

    for gene_info in panel.genes:
        gene = gene_info.gene

        # 2. gene 名が空文字でない
        if not gene or not isinstance(gene, str):
            raise ValueError(f"Invalid gene name: {gene}")

        # 3. 不正文字チェック
        if not pattern.match(gene):
            raise ValueError(f"Gene name contains invalid characters: {gene}")

        # 4. 重複チェック
        if gene in seen:
            raise ValueError(f"Duplicate gene name found: {gene}")
        seen.add(gene)

    # 5. 遺伝子数の上限
    if len(panel.genes) > 50:
        raise ValueError("Too many genes in panel")
