from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.passport import Passport
    from app.models.material import Material
    from app.models.aosr import Aosr


class AosrMaterial(Base):
    aosr_id: Mapped[int] = mapped_column(ForeignKey("aosrs.id"), nullable=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=True)
    volume: Mapped[float]

    aosr: Mapped["Aosr"] = relationship(back_populates="materials")
    material: Mapped["Material"] = relationship(back_populates="aosr_materials")
    passport: Mapped["Passport"] = relationship(back_populates="aosr_materials")
