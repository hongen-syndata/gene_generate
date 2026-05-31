from fastapi import FastAPI
from pydantic import BaseModel

from app.api.pipeline import run_pipeline_api

app = FastAPI()


class PipelineRequest(BaseModel):
    disease: str

@app.on_event("startup")
def startup_event():
    from app.db.session import engine
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)

@app.post("/pipeline/run")
def pipeline_endpoint(req: PipelineRequest):
    return run_pipeline_api(req.disease)

