import requests

from api.serializers import CreateWeatherInfoSerializer
from be.env import api_key
from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models import WeatherInfo


class WeatherService:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_info(self, page: int, page_size: int, data_body):
        query = self.db.query(WeatherInfo)
        filters = []

        data_body = dict(data_body)
        data_body.pop('access_token')

        for k, _ in data_body.items():
            if data_body.get(k) is not None:
                filters.append(getattr(WeatherInfo, k) == data_body.get(k))

        if filters:
            query = query.filter(and_(*filters))

        total = query.count()

        # Map page number to offset + 1, since offset always starts at 0 and page number starts at 1
        offset = (page - 1) * page_size if total > 0 else 0

        # Paginate all tasks into chunks of *page_size* objects
        users = query.offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size

        return query.all(), total, page, page_size, total_pages

    def create_weather_info(self, data_body):
        lat = data_body.__dict__.get('lat')
        lon = data_body.__dict__.get('lon')
        query = self.db.query(WeatherInfo)
        weather_info = query.filter(WeatherInfo.lat == lat, WeatherInfo.lon == lon).first()
        if weather_info:
            return weather_info
        open_weather_api = 'https://api.openweathermap.org/data/3.0/onecall'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'exclude': 'current,minutely,hourly,alerts'
        }

        result = requests.get(open_weather_api, params=params)
        print(result.text)
        if data := result.json():
            excluded_keys = {'hourly', 'daily', 'minutely', 'alerts', 'timezone_offset'}
            weather_data = {}
            current_data = data.get('current', {})

            for k, v in data.items():
                if k in excluded_keys:
                    continue
                if k == 'current':
                    continue
                weather_data[k] = v

            for info, value in current_data.items():
                if info == 'weather':
                    weather_data['weather'] = str(value) if value is not None else "[]"
                elif info == 'rain':
                    weather_data['rain'] = str(value) if value is not None else "[]"
                elif info in ['sunrise', 'sunset']:
                    weather_data[info] = int(value) if value is not None else 0
                elif info == 'dt':
                    weather_data['timestamp'] = int(value) if value is not None else 0
                else:
                    weather_data[info] = value if value is not None else 0

            new_weather_info = WeatherInfo(**weather_data)
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
