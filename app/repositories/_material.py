from app.repositories.base import BaseRepository
from app.models.material import Material
from app.schemas.material import MaterialSchema


class MaterialRepository(BaseRepository[Material, MaterialSchema]):
    Model = Material
    Schema = MaterialSchema
