from pydantic import BaseModel, Field


class Gene(BaseModel):
    name: str = Field(..., description="Gene symbol, e.g., BRCA1")
    transcript: str | None = Field(
        None, description="RefSeq transcript ID, e.g., NM_000000.0 (optional at MVP)"
    )
