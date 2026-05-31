import csv
import os
import re

from app.models.snp import SNP
from app.models.variant import Variant

# -----------------------------
# cDNA パーサー
# -----------------------------


def parse_snv(cdna: str):
    match = re.match(r"c\.(\d+)([ACGT])>([ACGT])", cdna)
    if not match:
        return None
    return {
        "pos": int(match.group(1)),
        "ref": match.group(2),
        "alt": match.group(3),
        "type": "substitution",
    }


def parse_del(cdna: str):
    match = re.match(r"c\.(\d+)del([ACGT])", cdna)
    if not match:
        return None
    return {"pos": int(match.group(1)), "ref": match.group(2), "alt": "-", "type": "deletion"}


PARSERS = [
    parse_snv,
    parse_del,
    # parse_ins,
    # parse_dup,
    # parse_delins,
]


def parse_cdna(cdna: str):
    cdna = cdna.strip()

    for parser in PARSERS:
        result = parser(cdna)
        if result is not None:
            return result

    return {"pos": None, "ref": None, "alt": None, "type": "unknown"}


# -----------------------------
# gene → chromosome 変換
# -----------------------------


def lookup_chromosome(gene: str) -> str | None:
    base_dir = os.path.dirname(__file__)  # app/services/
    csv_path = os.path.join(base_dir, "..", "..", "data", "gene_chromosome.csv")
    csv_path = os.path.abspath(csv_path)

    with open(csv_path, encoding="utf-8") as f:
        gene = gene.strip().upper()
        reader = csv.DictReader(f)
        for row in reader:
            if row["gene"].strip().upper() == gene:
                return row["chromosome"]
    return None


# -----------------------------
# SNP 生成（内部モデル対応）
# -----------------------------


def generate_snp(variants: list[Variant]) -> list[SNP]:
    snps: list[SNP] = []

    for var in variants:
        gene = var.gene
        chrom = lookup_chromosome(gene)

        parsed = parse_cdna(var.cDNA)

        snp = SNP(
            gene=gene,
            chrom=chrom,
            pos=parsed["pos"],
            ref=parsed["ref"],
            alt=parsed["alt"],
            type=parsed["type"],
            explanation=var.explanation,  # LLM 生成
        )

        snps.append(snp)

    return snps
