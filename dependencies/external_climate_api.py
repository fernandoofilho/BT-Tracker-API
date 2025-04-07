from interfaces.dependencies.IClimateApi import IClimateApi
class ExternalClimateApi(IClimateApi):
    def fetch_forecast(self, location: str) -> dict:
        # Simulate fetching forecast data from an external API
        return {
            "location": location,
            "temperature": 25,
            "humidity": 60,
            "condition": "Sunny"
        }

    def save_forecast_to_db(self, forecast_data: dict) -> None:
        # Simulate saving the forecast data to a database
        print(f"Saving forecast data to DB: {forecast_data}")