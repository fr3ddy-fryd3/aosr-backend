from .base import BaseSchema

# from .project_material import ProjectMaterialSchema, DBProjectMaterialSchema


class ProjectSchema(BaseSchema):
    name: str
    # materials: list[ProjectMaterialSchema]


class DBProjectSchema(BaseSchema):
    id: int
    name: str
    # materials: list[DBProjectMaterialSchema]


class DBProjectSchemaForUpdate(BaseSchema):
    id: int
    name: str
