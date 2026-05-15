# schemas/snp.py
from pydantic import BaseModel, Field


class SNP(BaseModel):
    gene: str = Field(..., description="Gene symbol, e.g., BRCA1")
    chrom: str = Field(..., description="Chromosome number as string, e.g., '17'")
    pos: int = Field(..., description="cDNA position (1-based)")
    ref: str = Field(..., description="Reference allele (A/C/G/T or '-')")
    alt: str = Field(..., description="Alternate allele (A/C/G/T or '-')")
    type: str = Field(..., description="Variant type: substitution, deletion, insertion, etc.")
    explanation: str | None = Field(
        default=None,
        description="LLM-generated explanation for the variant"
    )
