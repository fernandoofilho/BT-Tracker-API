from models import ApiForecastItem
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from dependencies.model import Model


class ProcessManyStates:
    @staticmethod
    async def get_days_without_rain(db_session: AsyncSession, date: str):
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d %H:%M").date()

            result = await db_session.execute(
                select(ApiForecastItem)
                .filter(ApiForecastItem.date_forecast <= target_date)
                .order_by(ApiForecastItem.date_forecast.desc())
            )
            items = result.scalars().all()

            days_without_rain = 0

            for item in items:
                item_date = datetime.strptime(
                    item.date_forecast, "%Y-%m-%d %H:%M"
                ).date()

                if item.precipitation < 0:
                    days_without_rain += 1
                else:
                    break

            return days_without_rain if days_without_rain > 0 else 0

        except Exception as e:
            print(f"Erro ao calcular dias sem chuva: {e}")
            return 0

    @staticmethod
    async def get(db_session: AsyncSession, date: str):
        model = Model()
        result = await db_session.execute(select(ApiForecastItem))
        items = result.scalars().all()
        items_list = []
        for item in items:
            item_date = datetime.strptime(
                item.date_forecast, "%Y-%m-%d %H:%M"
            ).date()
            input_date = datetime.strptime(date, "%Y-%m-%d %H:%M").date()
            if item_date == input_date:
                numero_dias_sem_chuva = await ProcessManyStates.get_days_without_rain(
                    db_session=db_session, date=date
                )

                result = model.predict(  
                    lat="0.5159170029240021",
                    lon="0.7610174486938237",
                    data_pas=item.date_forecast,
                    numero_dias_sem_chuva=numero_dias_sem_chuva,
                    precipitacao=item.precipitation,
                )
                print(f"\n\n\n result: {result} \n\n\n")
                # Garantir que o resultado seja serializável
                if isinstance(result, dict):
                    serialized_result = result
                else:
                    serialized_result = {
                        key: value for key, value in vars(result).items()
                    } if hasattr(result, "__dict__") else str(result)

                object_item = {
                    "result": serialized_result,
                    "local": "Manaus",
                    "date": item.date_forecast
                }
                items_list.append(object_item)
        return items_list
