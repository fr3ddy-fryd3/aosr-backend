from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.section import Section


class SectionMaterial(Base):
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"), index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("material.id"), index=True)
    volume: Mapped[int]

    section: Mapped["Section"] = relationship(back_populates="materials")
