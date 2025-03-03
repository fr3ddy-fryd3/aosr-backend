from typing import TYPE_CHECKING
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.material import Material
    from app.models.project import Project


class ProjectMaterial(Base):
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    volume: Mapped[float]

    project: Mapped["Project"] = relationship(back_populates="materials")
    material: Mapped["Material"] = relationship(back_populates="materials")
