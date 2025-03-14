from typing import TYPE_CHECKING

from .base import BaseSchema

if TYPE_CHECKING:
    from .aosr_material import AosrMaterialSchema, DBAosrMaterialSchema


class AosrSchema(BaseSchema):
    section_id: int
    name: str
    materials: list[AosrMaterialSchema]


class DBAosrSchema(BaseSchema):
    id: int
    section_id: int
    name: str
    materials: list[DBAosrMaterialSchema]
