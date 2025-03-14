from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

from app.models.section import Section
from app.models.project_material import ProjectMaterial

if TYPE_CHECKING:
    from app.models.passport import Passport


class Project(Base):
    name: Mapped[str] = mapped_column(unique=True)

    sections: Mapped[list["Section"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    materials: Mapped[list["ProjectMaterial"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
