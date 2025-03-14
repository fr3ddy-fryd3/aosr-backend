from .base import BaseSchema


class PassportSchema(BaseSchema):
    material_id: int
    number: int
    volume: int


class DBPassportSchema(PassportSchema):
    id: int
