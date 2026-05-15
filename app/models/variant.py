from pydantic import BaseModel, Field


class Variant(BaseModel):
    gene: str = Field(..., description="Gene symbol this variant belongs to, e.g., BRCA1")
    cDNA: str = Field(..., description="cDNA-level variant notation, e.g., c.123A>T")
    protein: str | None = Field(
        None, description="Protein-level notation, e.g., p.Lys41Asn (optional at MVP)"
    )
    type: str | None = Field(
        None, description="Variant type, e.g., missense, nonsense, deletion (optional at MVP)"
    )
    significance: str | None = Field(
        None, description="Clinical significance, e.g., Pathogenic (optional at MVP)"
    )
    explanation: str | None = Field(
        None, description="Brief explanation of clinical relevance (optional at MVP)"
    )
