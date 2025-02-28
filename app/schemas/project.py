from .base import BaseSchema


class ProjectSchema(BaseSchema):
    name: str
    materials: list[ProjectMaterialsSchema]


class DBProjectSchema(ProjectSchema):
    id: int
