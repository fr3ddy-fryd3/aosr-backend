from typing import TYPE_CHECKING
from .base import BaseSchema

if TYPE_CHECKING:
    from .material import DBMaterialSchema


class ProjectMaterialSchema(BaseSchema):
    project_id: int
    material_id: int
    volume: float


class DBProjectMaterialSchema(ProjectMaterialSchema):
    id: int
    material: DBMaterialSchema
