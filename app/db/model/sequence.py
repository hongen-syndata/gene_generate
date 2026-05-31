from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Sequence(Base):
    __tablename__ = "sequence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snp_id = Column(Integer, ForeignKey("snp.id"), nullable=False)

    ref_sequence = Column(String, nullable=False)
    alt_sequence = Column(String, nullable=False)

    snp = relationship("SNP", back_populates="sequence")
