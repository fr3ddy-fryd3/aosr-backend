import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    material_router,
    project_router,
    section_router,
    passport_router,
    passport_usage_router,
    aosr_router,
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.propagate = False

app = FastAPI()
app.include_router(material_router)
app.include_router(project_router)
app.include_router(section_router)
app.include_router(passport_router)
app.include_router(passport_usage_router)
app.include_router(aosr_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
