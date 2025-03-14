from typing import TYPE_CHECKING
from .base import BaseSchema
from .material import DBMaterialSchema


class SectionMaterialSchema(BaseSchema):
    section_id: int
    material_id: int
    volume: float


class DBSectionMaterialSchema(SectionMaterialSchema):
    id: int
    material: DBMaterialSchema
