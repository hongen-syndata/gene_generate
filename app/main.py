from fastapi import FastAPI
from pydantic import BaseModel

from app.api.pipeline import run_pipeline_api

app = FastAPI()


class PipelineRequest(BaseModel):
    disease: str


@app.post("/pipeline/run")
def pipeline_endpoint(req: PipelineRequest):
    return run_pipeline_api(req.disease)
