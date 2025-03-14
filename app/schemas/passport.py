from typing import TYPE_CHECKING

from .base import BaseSchema
from app.schemas.material import DBMaterialSchema


class PassportSchema(BaseSchema):
    material_id: int
    number: int
    volume: int


class DBPassportSchema(PassportSchema):
    id: int
    avaible_volume: int
    material: DBMaterialSchema
