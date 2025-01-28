from app.schemas import BaseSchema


class AosrMaterialSchema(BaseSchema):
    id: int | None = None
    aosr_id: int = 0
    material_id: int
    volume: int


class AosrMaterialWithNameSchema(AosrMaterialSchema):
    name: str
    units: str
