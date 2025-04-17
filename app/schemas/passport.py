from .base import BaseSchema
from app.schemas.material import DBMaterialSchema


class PassportSchema(BaseSchema):
    material_id: int
    number: str
    volume: float
    density: float


class PassportUsageSchema(BaseSchema):
    aosr_material_id: int
    passport_id: int
    used_volume: float


class DBPassportUsageSchema(PassportUsageSchema):
    id: int


class DBPassportSchema(PassportSchema):
    id: int
    available_volume: float
    material: DBMaterialSchema
