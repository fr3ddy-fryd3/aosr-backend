from .base import BaseSchema


class MaterialSchema(BaseSchema):
    name: str
    units: str


class DBMaterialSchema(MaterialSchema):
    id: int
