from typing import TYPE_CHECKING
from .base import BaseSchema

if TYPE_CHECKING:
    from .project_material import ProjectMaterialSchema, DBProjectMaterialSchema


class ProjectSchema(BaseSchema):
    name: str
    materials: list[ProjectMaterialSchema]


class DBProjectSchema(BaseSchema):
    id: int
    name: str
    materials: list[DBProjectMaterialSchema]
