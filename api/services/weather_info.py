from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models import WeatherInfo


class WeatherService:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_info(self, id=None, city=None, sunrise=None, sunset=None
                         , temp=None, feels_like=None, pressure=None, humidity=None
                         , dew_point=None, uvi=None, clouds=None, visibility=None
                         , wind_speed=None, wind_deg=None, wind_gust=None, weather=None
                         , pop=None):
        query = self.db.query(WeatherInfo)
        filters = []

        if id is not None:
            filters.append(WeatherInfo.id == id)
        if city is not None:
            filters.append(WeatherInfo.city == city)
        if sunrise is not None:
            filters.append(WeatherInfo.sunrise == sunrise)
        if sunset is not None:
            filters.append(WeatherInfo.sunset == sunset)
        if temp is not None:
            filters.append(WeatherInfo.temp == temp)
        if feels_like is not None:
            filters.append(WeatherInfo.feels_like == feels_like)
        if pressure is not None:
            filters.append(WeatherInfo.pressure == pressure)
        if humidity is not None:
            filters.append(WeatherInfo.humidity == humidity)
        if dew_point is not None:
            filters.append(WeatherInfo.dew_point == dew_point)
        if uvi is not None:
            filters.append(WeatherInfo.uvi == uvi)
        if clouds is not None:
            filters.append(WeatherInfo.clouds == clouds)
        if visibility is not None:
            filters.append(WeatherInfo.visibility == visibility)
        if wind_speed is not None:
            filters.append(WeatherInfo.wind_speed == wind_speed)
        if wind_deg is not None:
            filters.append(WeatherInfo.wind_deg == wind_deg)
        if wind_gust is not None:
            filters.append(WeatherInfo.wind_gust == wind_gust)
        if weather is not None:
            filters.append(WeatherInfo.weather == weather)
        if pop is not None:
            filters.append(WeatherInfo.pop == pop)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()

    def create_weather_info(self, data_body):
        new_weather_info = WeatherInfo(**data_body.dict())
        self.db.add(new_weather_info)
        self.db.commit()
        self.db.refresh(new_weather_info)

        return new_weather_info

    def update_weather_info(self, data_body):
        weather_info = self.db.query(WeatherInfo).filter(WeatherInfo.id == data_body).first()

        if weather_info is None:
            for key, value in data_body.items():
                if value is not None and key != 'id':
                    setattr(weather_info, key, value)
            self.db.commit()
            self.db.refresh(weather_info)

            return weather_info
        return None

    def delete_weather_info(self, id):
        weather_info = self.db.query(WeatherInfo).filter(WeatherInfo.id == id).first()

        if weather_info is not None:
            setattr(weather_info, 'is_deleted', True)
            self.db.commit()
            self.db.refresh(weather_info)

            return True
        return False
