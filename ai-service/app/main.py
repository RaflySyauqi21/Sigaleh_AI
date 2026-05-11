from fastapi import FastAPI
from datetime import datetime, timedelta

from app.schemas import (
    PredictionRequest,
    PredictionResponse,
    AutoPredictionRequest
)

from app.model_loader import (
    model,
    scaler
)

from app.inference import (
    predict_price
)

from app.data_pipeline import (
    fetch_commodities,
    fetch_weather,
    merge_data,
    build_model_input
)


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "SiGALEH AI Service Running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    try:
        predicted_price = predict_price(
            model,
            scaler,
            request.data
        )

    except Exception as e:
        return {
            "commodity": request.commodity,
            "city": request.city,
            "predicted_price": 0,
            "status": f"Error: {str(e)}"
        }

    last_price = request.data[-1][0]

    if predicted_price > last_price * 1.1:
        status = "Tinggi"
    elif predicted_price > last_price * 1.05:
        status = "Waspada"
    else:
        status = "Normal"

    return {
        "commodity": request.commodity,
        "city": request.city,
        "predicted_price": predicted_price,
        "status": status
    }


@app.post("/predict-auto", response_model=PredictionResponse)
def predict_auto(request: AutoPredictionRequest):

    try:
        end_date = datetime.today()

        for days in [60, 120, 180]:

            start_date = end_date - timedelta(days=days)

            commodities = fetch_commodities(
                request.city,
                request.commodity,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            weather = fetch_weather(
                request.city,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            merged = merge_data(commodities, weather)

            if len(merged) >= 30:
                break

        if len(merged) < 30:
            raise ValueError("Data tetap kurang meskipun sudah diperluas")

        model_input = build_model_input(merged)

        predicted_price = predict_price(
            model,
            scaler,
            model_input.tolist()
        )

    except Exception as e:
        return {
            "commodity": request.commodity,
            "city": request.city,
            "predicted_price": 0,
            "status": f"Error: {str(e)}"
        }

    last_price = merged[-1]["harga"]

    if predicted_price > last_price * 1.1:
        status = "Tinggi"
    elif predicted_price > last_price * 1.05:
        status = "Waspada"
    else:
        status = "Normal"

    return {
        "commodity": request.commodity,
        "city": request.city,
        "predicted_price": predicted_price,
        "status": status
    }