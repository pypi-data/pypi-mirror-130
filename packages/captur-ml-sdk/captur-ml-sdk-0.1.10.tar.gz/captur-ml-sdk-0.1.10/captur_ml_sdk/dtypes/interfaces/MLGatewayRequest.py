from pydantic import BaseModel
from typing import Optional

from request_parsers.meta import ModelRequestMetaField
from request_parsers.predict import ModelRequestPredictField
from request_parsers.train import ModelRequestTrainField
from request_parsers.evaluate import ModelRequestEvaluateField


class MLGatewayRequest(BaseModel):
    meta: Optional[ModelRequestMetaField]
    predict: Optional[ModelRequestPredictField]
    train: Optional[ModelRequestTrainField]
    evaluate: Optional[ModelRequestEvaluateField]


if __name__ == "__main__":
    print(MLGatewayRequest.schema_json(indent=2))
