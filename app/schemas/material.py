from app.schemas import BaseSchema


class MaterialSchema(BaseSchema):
    id: int | None = None
    name: str
    units: str


class MaterialWithVolumeSchema(MaterialSchema):
    volume: int
