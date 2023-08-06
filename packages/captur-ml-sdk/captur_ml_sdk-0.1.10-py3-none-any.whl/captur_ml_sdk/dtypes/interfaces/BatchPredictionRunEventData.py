from pydantic import BaseModel
from typing import Optional


class BatchPredictionRunEventData(BaseModel):
    gcs_source: str
    gcs_destination: str
    model_id: str
    job_display_name: str
    request_id: str
    labels_source: Optional[str]
    webhooks: str
