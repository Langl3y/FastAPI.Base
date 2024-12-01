import { Card, CardContent, Typography, Grid, Divider } from '@mui/material';
import { WeatherInfo } from '../types/api';

interface WeatherCardProps {
  weatherInfo: WeatherInfo;
}

export default function WeatherCard({ weatherInfo }: WeatherCardProps) {
  // Parse weather data from string
  const weatherData = weatherInfo.weather ? JSON.parse(weatherInfo.weather.replace(/'/g, '"'))[0] : null;

  return (
    <Card>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Location: {weatherInfo.lat}°, {weatherInfo.lon}°
            </Typography>
            <Divider sx={{ my: 1 }} />
          </Grid>
          
          {weatherInfo.temp !== null && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="primary">Temperature</Typography>
              <Typography>Temperature: {(weatherInfo.temp - 273.15).toFixed(1)}°C</Typography>
              {weatherInfo.feels_like !== null && (
                <Typography>Feels like: {(weatherInfo.feels_like - 273.15).toFixed(1)}°C</Typography>
              )}
              {weatherInfo.humidity !== null && (
                <Typography>Humidity: {weatherInfo.humidity}%</Typography>
              )}
            </Grid>
          )}

          {weatherData && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="primary">Conditions</Typography>
              <Typography>Description: {weatherData.description}</Typography>
              <Typography>Main: {weatherData.main}</Typography>
            </Grid>
          )}

          {weatherInfo.wind_speed !== null && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="primary">Wind</Typography>
              <Typography>Speed: {weatherInfo.wind_speed} m/s</Typography>
              {weatherInfo.wind_deg !== null && (
                <Typography>Direction: {weatherInfo.wind_deg}°</Typography>
              )}
            </Grid>
          )}

          {weatherInfo.timezone && (
            <Grid item xs={12}>
              <Divider sx={{ my: 1 }} />
              <Typography color="text.secondary">
                Timezone: {weatherInfo.timezone}
              </Typography>
              {weatherInfo.timestamp && (
                <Typography color="text.secondary">
                  Time: {new Date(weatherInfo.timestamp * 1000).toLocaleString()}
                </Typography>
              )}
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
}