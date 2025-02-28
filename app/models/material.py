from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.section_material import SectionMaterial
    from app.models.aosr_material import AosrMaterial


class Material(Base):
    name: Mapped[str] = mapped_column(unique=True)
    units: Mapped[str]

    section_materials: Mapped[list["SectionMaterial"]] = relationship(
        back_populates="material"
    )
    aosr_materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="material"
    )
