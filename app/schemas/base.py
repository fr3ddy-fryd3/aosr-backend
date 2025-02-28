from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # Для работы с ORM
        extra="ignore",  # Игнорировать неизвестные поля
        frozen=False,  # Разрешить изменение данных
        validate_default=True,  # Валидировать значения по умолчанию
    )
