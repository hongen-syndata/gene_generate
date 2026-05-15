from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Variant(Base):
    __tablename__ = "variant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gene_id = Column(Integer, ForeignKey("gene.id"), nullable=False)

    cDNA = Column(String, nullable=False)
    protein = Column(String)
    type = Column(String)
    significance = Column(String)
    explanation = Column(String)

    gene = relationship("Gene", back_populates="variants")
    snp = relationship("SNP", back_populates="variant", uselist=False)
