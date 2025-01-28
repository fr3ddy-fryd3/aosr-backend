from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.section_material import SectionMaterial


class Section(Base):
    name: Mapped[str] = mapped_column(unique=True)

    materials: Mapped[list["SectionMaterial"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )
