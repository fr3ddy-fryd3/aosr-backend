from .base import BaseSchema


class MaterialSchema(BaseSchema):
    name: str
    units: str
    density: float


class DBMaterialSchema(MaterialSchema):
    id: int
