from abc import ABC, abstractmethod
class IClimateApi(ABC):
    @abstractmethod
    def fetch_forecast(): pass 
    def save_forecast_to_db(): pass
    pass 