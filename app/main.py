from fastapi import FastAPI

from app.routers.v1 import router as v1_router
from app.database.session import Base, create_database_schema, engine

create_database_schema()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalone API", version="1.0.0")
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
