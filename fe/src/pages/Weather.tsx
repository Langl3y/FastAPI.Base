import { Box, Typography, Grid, CircularProgress, Button, Stack } from '@mui/material';
import { Refresh } from '@mui/icons-material';
import { useWeatherInfo } from '../hooks/useWeatherInfo';
import WeatherForm from '../components/WeatherForm';
import WeatherCard from '../components/WeatherCard';
import { useEffect } from 'react';
import { WeatherInfo } from '../types/api';
import { weatherApi } from '../services/api';
import { useNotification } from '../contexts/NotificationContext';

// Helper function to count non-null values
const countNonNullValues = (obj: Record<string, any>): number => {
  return Object.values(obj).filter(value => value !== null).length;
};

// Helper function to filter weather data
const filterWeatherData = (data: WeatherInfo[]): WeatherInfo[] => {
  // Group by timezone
  const groupedByTimezone = data.reduce((acc, item) => {
    if (!acc[item.timezone]) {
      acc[item.timezone] = [];
    }
    acc[item.timezone].push(item);
    return acc;
  }, {} as Record<string, WeatherInfo[]>);

  // For each timezone, keep only the entry with the most non-null values
  return Object.values(groupedByTimezone).map(group => 
    group.reduce((best, current) => 
      countNonNullValues(current) > countNonNullValues(best) ? current : best
    )
  );
};

const LOCATION_THRESHOLD = 0.1; // Threshold for considering locations as "same" (in degrees)

export default function Weather() {
  const { weatherInfo, isLoading, createWeatherInfo, fetchWeatherInfo } = useWeatherInfo();
  const { showNotification } = useNotification();

  useEffect(() => {
    console.log('Current weather info:', weatherInfo);
  }, [weatherInfo]);

  // Helper function to find existing weather record
  const findExistingRecord = (lat: number, lon: number): WeatherInfo | undefined => {
    return weatherInfo.find(info => 
      Math.abs(info.lat - lat) < LOCATION_THRESHOLD && 
      Math.abs(info.lon - lon) < LOCATION_THRESHOLD
    );
  };

  const handleSubmit = async (values: { lat: number; lon: number }) => {
    try {
      // First check if we have existing data for this location
      const existingRecord = findExistingRecord(values.lat, values.lon);
      
      if (existingRecord) {
        // If exists, update it
        await weatherApi.updateWeatherInfo(existingRecord.id);
        showNotification('Weather information updated successfully', 'success');
      } else {
        // If doesn't exist, create new
        await createWeatherInfo(values);
      }
      
      // Refresh the data
      await fetchWeatherInfo();
    } catch (error: any) {
      console.error('Weather operation failed:', error);
      showNotification(error.message || 'Failed to process weather information', 'error');
    }
  };

  const handleRefresh = async () => {
    try {
      // Get current weather data
      const result = await fetchWeatherInfo();
      const currentData = result.data || [];
      
      // Update all existing records
      for (const record of currentData) {
        await weatherApi.updateWeatherInfo(record.id);
      }
      
      // Fetch updated data
      await fetchWeatherInfo();
      showNotification('All weather information updated successfully', 'success');
    } catch (error: any) {
      console.error('Refresh error:', error);
      showNotification(error.message || 'Failed to refresh weather information', 'error');
    }
  };

  // Filter the weather data before rendering
  const filteredWeatherInfo = filterWeatherData(weatherInfo);

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Typography variant="h5">
          Weather Information
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          disabled={isLoading}
        >
          Refresh Data
        </Button>
      </Stack>

      <WeatherForm onSubmit={handleSubmit} />

      {isLoading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={2} sx={{ mt: 2 }}>
          {Array.isArray(filteredWeatherInfo) && filteredWeatherInfo.map((info) => (
            <Grid item xs={12} md={6} key={info.id}>
              <WeatherCard weatherInfo={info} />
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}