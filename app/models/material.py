from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Material(Base):
    name: Mapped[str] = mapped_column(unique=True)
    units: Mapped[str]
