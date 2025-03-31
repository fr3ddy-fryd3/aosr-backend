from typing import TYPE_CHECKING

from .base import BaseSchema
from app.schemas.material import DBMaterialSchema


class PassportSchema(BaseSchema):
    material_id: int
    number: str
    volume: float


class DBPassportSchema(PassportSchema):
    id: int
    available_volume: float
    material: DBMaterialSchema


class PassportUsageSchema(BaseSchema):
    aosr_material_id: int
    passport_id: int
    used_volume: int


class DBPassportUsageSchema(PassportUsageSchema):
    id: int
