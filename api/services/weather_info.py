import requests

from api.serializers import CreateWeatherInfoSerializer
from be.env import api_key
from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models import WeatherInfo

from api.common.responses import APIResponseCode
from api.common.responses import APIResponseCode

class WeatherService:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_info(self, page: int, page_size: int, data_body):
        try:
            query = self.db.query(WeatherInfo).filter(WeatherInfo.is_deleted == False)
            
            # Only use valid model fields for filtering
            valid_fields = ['id', 'lat', 'lon', 'timestamp', 'timezone']
            data_dict = data_body.dict(exclude={'access_token', 'page', 'page_size'})
            
            filters = []
            for key, value in data_dict.items():
                if value is not None and key in valid_fields:
                    filters.append(getattr(WeatherInfo, key) == value)

            if filters:
                query = query.filter(and_(*filters))

            total = query.count()
            offset = (page - 1) * page_size if total > 0 else 0
            results = query.offset(offset).limit(page_size).all()
            total_pages = (total + page_size - 1) // page_size

            return results, total, page, page_size, total_pages
        except Exception as e:
            self.db.rollback()
            raise Exception(f"{APIResponseCode.DATABASE_ERROR['message']}: {str(e)}")

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
        try:
            weather_id = data_body.id
            weather_info = self.db.query(WeatherInfo).filter(
                WeatherInfo.id == weather_id,
                WeatherInfo.is_deleted == False
            ).first()
            
            if weather_info is None:
                raise ValueError(f"Weather info with id {weather_id} not found")

            # Fetch fresh data from OpenWeather API
            open_weather_api = 'https://api.openweathermap.org/data/3.0/onecall'
            params = {
                'lat': weather_info.lat,
                'lon': weather_info.lon,
                'appid': api_key,
                'exclude': 'minutely,hourly,alerts'
            }

            response = requests.get(open_weather_api, params=params)
            if not response.ok:
                raise Exception(f"OpenWeather API error: {response.text}")

            data = response.json()
            daily_data = data.get('daily', [])[0] if data.get('daily') else {}
            
            # Update weather info with fresh data
            weather_data = {
                'timezone': data.get('timezone', ''),
                'timestamp': daily_data.get('dt', 0),
                'sunrise': daily_data.get('sunrise', 0),
                'sunset': daily_data.get('sunset', 0),
                'temp': daily_data.get('temp', {}).get('day', 0),
                'feels_like': daily_data.get('feels_like', {}).get('day', 0),
                'pressure': daily_data.get('pressure', 0),
                'humidity': daily_data.get('humidity', 0),
                'dew_point': daily_data.get('dew_point', 0),
                'uvi': daily_data.get('uvi', 0),
                'clouds': daily_data.get('clouds', 0),
                'visibility': data.get('current', {}).get('visibility', 0),
                'wind_speed': daily_data.get('wind_speed', 0),
                'wind_deg': daily_data.get('wind_deg', 0),
                'wind_gust': daily_data.get('wind_gust', 0),
                'weather': str(daily_data.get('weather', [])),
                'pop': daily_data.get('pop', 0),
                'rain': str(daily_data.get('rain', 0))
            }

            # Update the database record
            for key, value in weather_data.items():
                setattr(weather_info, key, value)
                
            self.db.commit()
            self.db.refresh(weather_info)

            return weather_info
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_weather_info(self, id):
        weather_info = self.db.query(WeatherInfo).filter(WeatherInfo.id == id).first()

        if weather_info is not None:
            setattr(weather_info, 'is_deleted', True)
            self.db.commit()
            self.db.refresh(weather_info)

            return True
        return False
