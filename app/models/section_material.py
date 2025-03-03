from typing import TYPE_CHECKING
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.material import Material
    from app.models.section import Section


class SectionMaterial(Base):
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    volume: Mapped[float]

    section: Mapped["Section"] = relationship(back_populates="materials")
    material: Mapped["Material"] = relationship(back_populates="materials")
