from pydantic import BaseModel, Field


class VariantInfo(BaseModel):
    cDNA: str = Field(..., description="cDNA-level variant notation, e.g., c.123A>T")
    protein: str = Field(..., description="Protein-level variant notation, e.g., p.Lys41Asn")
    type: str = Field(..., description="Variant type, e.g., missense, nonsense, deletion")
    significance: str = Field(..., description="Clinical significance, e.g., Pathogenic")
    explanation: str = Field(..., description="Brief explanation of clinical relevance")

class GeneInfo(BaseModel):
    gene: str = Field(..., description="Gene symbol, e.g., BRCA1")
    transcript: str = Field(..., description="RefSeq transcript ID, e.g., NM_000000.0")
    variants: list[VariantInfo] = Field(..., description="List of variants associated with the gene")

class Panel(BaseModel):
    disease: str = Field(..., description="Disease name, e.g., Breast cancer")
    generated_at: str = Field(..., description="Timestamp when the panel was generated")
    genes: list[GeneInfo] = Field(..., description="List of genes associated with the disease")
