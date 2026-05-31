from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class SNP(Base):
    __tablename__ = "snp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variant.id"), nullable=False)

    ref = Column(String, nullable=False)
    alt = Column(String, nullable=False)
    pos = Column(Integer, nullable=False)

    variant = relationship("Variant", back_populates="snp")
    sequence = relationship("Sequence", back_populates="snp", uselist=False)
