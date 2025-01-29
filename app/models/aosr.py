from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.aosr_material import AosrMaterial


class Aosr(Base):
    name: Mapped[str] = mapped_column()
    section_id: Mapped[int] = mapped_column(
        ForeignKey("section.id"), index=True)

    materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="aosr", cascade="all, delete-orphan"
    )
