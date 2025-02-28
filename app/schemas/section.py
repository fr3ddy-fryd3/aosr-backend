from .base import BaseSchema


class SectionSchema(BaseSchema):
    project_id: int
    name: str
