from typing import TYPE_CHECKING
from .base import BaseSchema

from .material import DBMaterialSchema


class ProjectMaterialSchema(BaseSchema):
    material_id: int
    volume: float


class DBProjectMaterialSchema(ProjectMaterialSchema):
    id: int
    project_id: int
    material: DBMaterialSchema
