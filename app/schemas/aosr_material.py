from typing import TYPE_CHECKING
from .base import BaseSchema

if TYPE_CHECKING:
    from .material import DBMaterialSchema


class AosrMaterialSchema(BaseSchema):
    material_id: int
    volume: float


class DBAosrMaterialSchema(AosrMaterialSchema):
    id: int
    aosr_id: int
    material: DBMaterialSchema
    used_volume: int
