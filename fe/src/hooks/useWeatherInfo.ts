import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { weatherApi } from '../services/api';
import { useNotification } from '../contexts/NotificationContext';
import { WeatherInfo } from '../types/api';

export function useWeatherInfo() {
  const queryClient = useQueryClient();
  const { showNotification } = useNotification();

  const { data: weatherInfo = [], isLoading, error, refetch: fetchWeatherInfo } = useQuery<WeatherInfo[], Error>({
    queryKey: ['weather'],
    queryFn: async () => {
      const data = await weatherApi.getWeatherInfo();
      console.log('Fetched weather data:', data);
      return data;
    },
    refetchOnWindowFocus: false,
    retry: false
  });

  const createWeatherInfoMutation = useMutation({
    mutationFn: weatherApi.createWeatherInfo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['weather'] });
      showNotification('Weather information added successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to create weather info', 'error');
    }
  });

  const updateWeatherInfoMutation = useMutation({
    mutationFn: weatherApi.updateWeatherInfo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['weather'] });
      showNotification('Weather information updated successfully', 'success');
    },
    onError: (error: Error) => {
      showNotification(error.message || 'Failed to update weather info', 'error');
    }
  });

  useEffect(() => {
    if (error) {
      showNotification(error.message || 'Failed to fetch weather info', 'error');
    }
  }, [error, showNotification]);

  return {
    weatherInfo,
    isLoading,
    error,
    createWeatherInfo: createWeatherInfoMutation.mutateAsync,
    updateWeatherInfo: updateWeatherInfoMutation.mutateAsync,
    fetchWeatherInfo
  };
}