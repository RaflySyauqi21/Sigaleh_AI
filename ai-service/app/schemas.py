from pydantic import BaseModel, field_validator
from typing import List


class PredictionRequest(BaseModel):

    commodity: str
    city: str
    data: List[List[float]]

    @field_validator('data')
    @classmethod
    def validate_data(cls, v):

        if len(v) != 30:
            raise ValueError("Data harus 30 timestep")

        for row in v:
            if len(row) != 5:
                raise ValueError("Setiap timestep harus 5 fitur")

        return v


class AutoPredictionRequest(BaseModel):

    commodity: str
    city: str


class PredictionResponse(BaseModel):

    commodity: str
    city: str
    predicted_price: float
    status: str