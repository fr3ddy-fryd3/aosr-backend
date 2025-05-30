from .base import BaseSchema
from .material import DBMaterialSchema


class SectionMaterialSchema(BaseSchema):
    section_id: int
    material_id: int
    volume: float


class DBSectionMaterialSchema(SectionMaterialSchema):
    id: int
    material: DBMaterialSchema


class DBSectionMaterialSchemaForUpdate(SectionMaterialSchema):
    id: int
    section_id: int
