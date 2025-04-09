from .base import BaseSchema
from app.schemas.passport import DBPassportUsageSchema

from .section_material import DBSectionMaterialSchema


class AosrMaterialSchema(BaseSchema):
    aosr_id: int
    section_material_id: int
    volume: float


class DBAosrMaterialSchema(AosrMaterialSchema):
    id: int
    section_material: DBSectionMaterialSchema
    used_volume: float
    passport_usages: list[DBPassportUsageSchema]


class DBAosrMaterialSchemaForUpdate(AosrMaterialSchema):
    id: int
