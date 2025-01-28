from app.schemas.section_material import SectionMaterialWithNameSchema
from app.schemas import BaseSchema


class SectionSchema(BaseSchema):
    id: int | None = None
    name: str


class SectionWithMaterialsSchema(SectionSchema):
    materials: list[SectionMaterialWithNameSchema]
