from .base import BaseSchema
from .aosr_material import AosrMaterialSchema, DBAosrMaterialSchema


class AosrSchema(BaseSchema):
    section_id: int
    name: str


class DBAosrSchema(BaseSchema):
    id: int
    section_id: int
    name: str
    materials: list[DBAosrMaterialSchema]


class DBAosrSchemaWithoutMaterials(BaseSchema):
    id: int
    section_id: int
    name: str
