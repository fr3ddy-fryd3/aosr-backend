from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.section import Section
    from app.models.aosr_material import AosrMaterial


class Aosr(Base):
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"), nullable=False)
    name: Mapped[str]

    section: Mapped["Section"] = relationship(back_populates="aosrs")
    materials: Mapped[list["AosrMaterial"]] = relationship(
        back_populates="aosr", cascade="all, delete-orphan"
    )
