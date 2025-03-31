from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

from app.models.project_material import ProjectMaterial
from app.models.section_material import SectionMaterial
from app.models.aosr_material import AosrMaterial

if TYPE_CHECKING:
    from app.models.passport import Passport


class Material(Base):
    name: Mapped[str] = mapped_column(unique=True)
    units: Mapped[str]
    density: Mapped[float]

    project_materials: Mapped[list["ProjectMaterial"]] = relationship(
        back_populates="material"
    )
    section_materials: Mapped[list["SectionMaterial"]] = relationship(
        back_populates="material"
    )
    aosr_materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="material"
    )
    passports: Mapped[list["Passport"]] = relationship(
        back_populates="material", cascade="all, delete-orphan"
    )
