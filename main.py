from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    material_router,
    project_router,
    section_router,
    passport_router,
)


app = FastAPI()
app.include_router(material_router)
app.include_router(project_router)
app.include_router(section_router)
app.include_router(passport_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.10.85:8080"],  # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
