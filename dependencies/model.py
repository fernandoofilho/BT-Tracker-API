import pickle
import pandas as pd
import os
from dotenv import load_dotenv
from joblib import load

load_dotenv()
class Model:
    def __init__(self, model_path = os.getenv("MODEL_PATH")):
        self.model_path =  model_path 
        self.model = self.__load_model()

    
    def __load_model(self):
        try:
            model = load(self.model_path)
            if not hasattr(model, "predict"):
                raise Exception("Loaded object is not a valid model with a 'predict' method.")
            return model
        except FileNotFoundError:
            raise Exception(f"Model file not found at {self.model_path}")
        except Exception as e:
            raise Exception(f"{e}")

    def predict(self, lat, lon, data_pas, numero_dias_sem_chuva, precipitacao):
        input_data = pd.DataFrame({
            'lat': [float(lat)],
            'lon': [float(lon)],
            'data_pas': data_pas,
            'pais': "Brasil",
            'numero_dias_sem_chuva': [float(numero_dias_sem_chuva)],
            'precipitacao': [float(precipitacao)],
        })

        input_data["data_pas"] = pd.to_datetime(input_data["data_pas"])
        # input_data["month"] = input_data["data_pas"].dt.month
        # input_data["day_of_year"] = input_data["data_pas"].dt.dayofyear

        # input_data = input_data.drop(columns=["data_pas"])

        # expected_columns = ['lat', 'lon', 'numero_dias_sem_chuva', 'precipitacao', 'data_pas']
        # input_data = input_data[expected_columns]

        try:
            prediction = self.model.predict(input_data)
            return int(prediction[0])
        except Exception as e:
            raise Exception(f"Error during prediction: {e}")

    def prepare_input(self, climate_data, lat, lon):
        try:
            data_1h = climate_data.get("data_1h", {})
            precipitation_data = data_1h.get("precipitation", [])
            
            if not precipitation_data or len(precipitation_data) < 24 * 7:
                raise ValueError("Dados de precipitação insuficientes para 7 dias")

            input_data_dict = {}

            for i in range(7):
                start = i * 24
                end = (i + 1) * 24
                precipitacoes = precipitation_data[start:end]

                registros_dia = []
                for j in range(24): 
                    input_data = {
                        "lat": lat,
                        "lon": lon,
                        "data_pas": climate_data["metadata"].get("modelrun_updatetime_utc", "N/A"),
                        "hora": j, 
                        "precipitacao": precipitacoes[j],
                        "numero_dias_sem_chuva": precipitacoes[j] == 0 
                    }
                    registros_dia.append(input_data)

                input_data_dict[f"d{i+1}"] = registros_dia 
            
            return input_data_dict

        except KeyError as e:
            raise ValueError(f"Chave ausente nos dados climáticos: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Erro ao processar os dados: {str(e)}")
