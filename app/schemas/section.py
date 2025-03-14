from typing import TYPE_CHECKING
from .base import BaseSchema
from .section_material import DBSectionMaterialSchema, SectionMaterialSchema


class SectionSchema(BaseSchema):
    project_id: int
    name: str
    materials: list[SectionMaterialSchema]


class DBSectionSchema(BaseSchema):
    id: int
    project_id: int
    name: str
    materials: list[DBSectionMaterialSchema]
