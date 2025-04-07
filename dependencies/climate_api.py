
from dotenv import load_dotenv
import os
import requests
from sqlalchemy.orm import Session
from db import SessionLocal
from models import ApiForecastHeader, Units, ApiForecastItem

load_dotenv()
API_SECRET = os.getenv("API_KEY")
SHARED_SECRET = os.getenv("API_SHARED_SECRET")
API_URL = os.getenv("API_URL")



class ClimateApi:
    def __init__(self):
        self.api_secret = API_SECRET
        self.shared_secret = SHARED_SECRET

    def __get_signature(self, query: str) -> str:
        import hashlib
        import hmac
        return hmac.new(self.shared_secret.encode(), query.encode(), hashlib.sha256).hexdigest()

    def fetch_forecast(self, lat: float, lon: float, expire: int = 1924948800) -> dict:
        query = f"/packages/basic-1h?lat={lat}&lon={lon}&apikey={self.api_secret}&expire={expire}"
        signature = self.__get_signature(query)
        url = f"https://my.meteoblue.com{query}&sig={signature}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    async def save_forecast_to_db(self, data: dict, lat: float, lon: float):
        async with SessionLocal() as session:
            header = ApiForecastHeader(
                modelrun=data["metadata"].get("modelrun_updatetime_utc"),
                name=data["metadata"].get("name"),
                height=data["metadata"].get("height"),
                timezone_abbrevation=data["metadata"].get("timezone_abbrevation"),
                latitude=lat,
                longitude=lon,
                modelrun_utc=data["metadata"].get("modelrun_utc"),
                utc_timeoffset=data["metadata"].get("utc_timeoffset"),
                generation_time_ms=data["metadata"].get("generation_time_ms")
            )
            session.add(header)
            await session.commit()
            session.refresh(header)
            
            units = Units(
                modelrun=data["metadata"].get("modelrun_updatetime_utc"),
                precipitation=data["units"].get("precipitation"),
                windspeed=data["units"].get("windspeed"),
                precipitation_probability=data["units"].get("precipitation_probability"),
                relativehumidity=data["units"].get("relativehumidity"),
                temperature=data["units"].get("temperature"),
                time=data["units"].get("time"),
                pressure=data["units"].get("pressure"),
                winddirection=data["units"].get("winddirection")
            )
            session.add(units)

            await session.commit()
            session.refresh(units)

            for i, time in enumerate(data["data_1h"]["time"]):
                forecast_item = ApiForecastItem(
                    modelrun=data["metadata"].get("modelrun_updatetime_utc"),
                    date_forecast=time,
                    windspeed=data["data_1h"].get("windspeed", [None])[i],
                    temperature=data["data_1h"].get("temperature", [None])[i],
                    precipitation_probability=data["data_1h"].get("precipitation_probability", [None])[i],
                    convective_precipitation=data["data_1h"].get("convective_precipitation", [None])[i],
                    rainspot=data["data_1h"].get("rainspot", [None])[i],
                    pictocode=data["data_1h"].get("pictocode", [None])[i],
                    felttemperature=data["data_1h"].get("felttemperature", [None])[i],
                    precipitation=data["data_1h"].get("precipitation", [None])[i],
                    isdaylight=data["data_1h"].get("isdaylight", [None])[i],
                    uvindex=data["data_1h"].get("uvindex", [None])[i],
                    relativehumidity=data["data_1h"].get("relativehumidity", [None])[i],
                    sealevelpressure=data["data_1h"].get("sealevelpressure", [None])[i],
                    winddirection=data["data_1h"].get("winddirection", [None])[i]
                )
                session.add(forecast_item)

            await session.commit()