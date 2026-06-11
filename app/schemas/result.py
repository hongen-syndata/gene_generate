from pydantic import BaseModel, Field


class GeneResult(BaseModel):
    gene: str = Field(..., description="Gene symbol, e.g., TP53")
    significance: str | None = Field(
        None, description="Clinical significance, e.g., Pathogenic"
    )
    explanation: str | None = Field(
        None, description="Brief explanation of clinical relevance (LLM generated)"
    )
    sequence: str = Field(
        ..., description="ALT (mutated) nucleotide sequence as raw A/T/C/G bases"
    )


class PipelineResult(BaseModel):
    disease: str = Field(..., description="Disease name, e.g., Breast cancer")
    results: list[GeneResult] = Field(
        ..., description="Per-variant gene / significance / sequence results"
    )
