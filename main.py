from fastapi import FastAPI, Request, Depends
from models import PayloadBody
from dependencies.climate_api import ClimateApi
from dependencies.model import Model
from db import SessionLocal
from helpers.processManyStates import ProcessManyStates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from serializer import Serializer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI(
    title="AI4GOOD Fire Risk API",
    description="API para inferência de risco de fogo com dados climáticos e modelo AI",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model_ai = Model()
climate_api = ClimateApi()


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.get("/", tags=["Root"])
def read_root():
    return {"root": "Hello AI4GOOD"}


@app.get("/fireRisk/", tags=["Fire Risk"])
async def inferir_todos(db: AsyncSession = Depends(get_db)):
    data = await ProcessManyStates.get(date="2024-12-08 00:00", db_session=db)
    return Serializer.serialize_many(data)


@app.post("/fireRisk/detail", tags=["Fire Risk"])
def inferir(input_data: PayloadBody):
    data = model_ai.predict(input_data)
    return Serializer.serialize_data(data)


@app.post("/api_climate/data", tags=["Climate"])
async def get_climate_data(request: Request):
    input_data = await request.json()
    try:
        lat = input_data["lat"]
        lon = input_data["lon"]
        data = climate_api.fetch_forecast(lat, lon)
        await climate_api.save_forecast_to_db(data, lat, lon)
    except Exception as e:
        data = {"erro": f"Error during fetch data: {e}"}
    return data


@app.get("/predict", tags=["Prediction"])
async def get_prediction(lat: float, lon: float, db: AsyncSession = Depends(get_db)):
    climate_data = climate_api.fetch_forecast(lat, lon)
    input_data = model_ai.prepare_input(climate_data, lat=lat, lon=lon)
    response = []
    for day in input_data.keys():
        prediction_array = []
        for entry in input_data[day]:
            prediction = model_ai.predict(
                lat=lat,
                lon=lon,
                data_pas=entry["data_pas"],
                numero_dias_sem_chuva=entry["numero_dias_sem_chuva"],
                precipitacao=entry["precipitacao"],
            )
            prediction_array.append(prediction)
        count_zeros = prediction_array.count(0)
        count_ones = prediction_array.count(1)
        response.append(
            {f"{entry['data_pas']}": [1] if count_ones > count_zeros else [0]}
        )
    return Serializer.serialize_data(response)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
