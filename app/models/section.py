from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base
from app.models.aosr import Aosr
from app.models.section_material import SectionMaterial

if TYPE_CHECKING:
    from app.models.project import Project


class Section(Base):
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(unique=True)

    project: Mapped["Project"] = relationship(back_populates="sections")
    aosrs: Mapped[list["Aosr"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )
    materials: Mapped[list["SectionMaterial"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )
