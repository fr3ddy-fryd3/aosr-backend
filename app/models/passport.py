from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from app.models.aosr_material import AosrMaterial
from app.models.base import Base
from app.models.project import Project
from app.models.section import Section


class Passport(Base):
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    number: Mapped[int] = mapped_column(unique=True)
    volume: Mapped[int]

    projects: Mapped[list["Project"]] = relationship(
        back_populates="passports", cascade="all"
    )
    sections: Mapped[list["Section"]] = relationship(
        back_populates="passports", cascade="all"
    )
    aosr_materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="passport", cascade="all"
    )
