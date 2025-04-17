from .base import BaseSchema
from .section_material import DBSectionMaterialSchema, SectionMaterialSchema


class SectionSchema(BaseSchema):
    project_id: int
    name: str


class DBSectionSchema(BaseSchema):
    id: int
    project_id: int
    name: str
    materials: list[DBSectionMaterialSchema]


class DBSectionSchemaForCreate(BaseSchema):
    id: int
    project_id: int
    name: str
