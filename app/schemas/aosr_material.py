from typing import TYPE_CHECKING
from .base import BaseSchema

if TYPE_CHECKING:
    from .material import DBMaterialSchema


class AosrMaterialSchema(BaseSchema):
    aosr_id: int
    material_id: int
    volume: float


class DBAosrMaterialSchema(AosrMaterialSchema):
    id: int
    material: DBMaterialSchema
