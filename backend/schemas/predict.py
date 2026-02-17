from pydantic import BaseModel

class PredictResponse(BaseModel):
    filename: str
    prediction: str
    confidence: str