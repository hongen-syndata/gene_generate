from pydantic import BaseModel, Field


class SequenceResult(BaseModel):
    fasta_ref: str = Field(..., description="FASTA Refernce sequence (A/T/C/G)")
    fasta_alt: str = Field(..., description="FASTA Alternate sequence (A/T/C/G)")
