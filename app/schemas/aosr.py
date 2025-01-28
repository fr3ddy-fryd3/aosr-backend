from app.schemas.aosr_material import AosrMaterialSchema
from app.schemas import BaseSchema


class AosrSchema(BaseSchema):
    id: int | None = None
    name: str
    section_id: int


class AosrWithMaterialsSchema(AosrSchema):
    materials: list[AosrMaterialSchema]
