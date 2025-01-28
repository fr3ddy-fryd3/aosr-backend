from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    material_router,
    section_router,
    section_material_router,
    aosr_router,
    aosr_material_router,
)


app = FastAPI()
app.include_router(material_router)
app.include_router(section_router)
app.include_router(section_material_router)
app.include_router(aosr_router)
app.include_router(aosr_material_router)

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
