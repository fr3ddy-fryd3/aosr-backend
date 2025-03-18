from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from app.models.aosr_material import AosrMaterial
from app.models.base import Base
from app.models.material import Material


class Passport(Base):
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    number: Mapped[str] = mapped_column(unique=True)
    volume: Mapped[int]

    aosr_usages: Mapped[list["PassportUsage"]] = relationship(back_populates="passport")
    material: Mapped["Material"] = relationship(back_populates="passports")

    @property
    def available_volume(self) -> int:
        used_volume = sum(usage.used_volume for usage in self.aosr_usages)
        return self.volume - used_volume


class PassportUsage(Base):
    aosr_material_id: Mapped[int] = mapped_column(ForeignKey("aosrmaterials.id"))
    passport_id: Mapped[int] = mapped_column(ForeignKey("passports.id"))
    used_volume: Mapped[int] = mapped_column(nullable=False)

    aosr_material: Mapped["AosrMaterial"] = relationship(
        back_populates="passport_usages"
    )
    passport: Mapped["Passport"] = relationship(back_populates="aosr_usages")
