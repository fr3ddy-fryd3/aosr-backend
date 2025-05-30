from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.passport import PassportUsage
    from app.models.section_material import SectionMaterial
    from app.models.aosr import Aosr


class AosrMaterial(Base):
    aosr_id: Mapped[int] = mapped_column(ForeignKey("aosrs.id"))
    section_material_id: Mapped[int] = mapped_column(ForeignKey("sectionmaterials.id"))
    volume: Mapped[float]

    aosr: Mapped["Aosr"] = relationship(back_populates="materials")
    section_material: Mapped["SectionMaterial"] = relationship(
        back_populates="aosr_materials"
    )
    passport_usages: Mapped[list["PassportUsage"]] = relationship(
        back_populates="aosr_material", cascade="all, delete-orphan"
    )

    @property
    def used_volume(self) -> float:
        return sum(usage.used_volume for usage in self.passport_usages)
