from .base import BaseSchema
from .material import DBMaterialSchema


class SectionMaterialSchema(BaseSchema):
    material_id: int
    volume: float


class DBSectionMaterialSchema(SectionMaterialSchema):
    id: int
    section_id: int
    material: DBMaterialSchema
