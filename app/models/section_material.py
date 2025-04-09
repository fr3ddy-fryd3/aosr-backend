from typing import TYPE_CHECKING
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.aosr_material import AosrMaterial
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.material import Material
    from app.models.section import Section


class SectionMaterial(Base):
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"), nullable=False, unique=True
    )
    volume: Mapped[float]

    section: Mapped["Section"] = relationship(back_populates="materials")
    material: Mapped["Material"] = relationship(back_populates="section_materials")
    aosr_materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="section_material", cascade="all, delete-orphan"
    )
