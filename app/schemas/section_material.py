from app.schemas import BaseSchema


class SectionMaterialSchema(BaseSchema):
    id: int | None = None
    section_id: int = 0
    material_id: int | None = None
    volume: int


# Эта схема нужна для отправки данных на фронт в более удобном виде
class SectionMaterialWithNameSchema(SectionMaterialSchema):
    name: str
    units: str
