import axios from 'axios';
import { User, Task, WeatherInfo } from '../types/api';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Add request interceptor to include token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const tasksApi = {
  getTasks: () => api.post<Task[]>('/api/tasks/get_tasks').then(res => res.data),
  createTask: (task: Omit<Task, 'id'>) => api.post<Task>('/api/tasks/create_task', task).then(res => res.data),
  updateTask: (task: { id: number } & Partial<Task>) => api.post<Task>('/api/tasks/update_task', task).then(res => res.data),
  deleteTask: (id: number) => api.post('/api/tasks/delete_task', { id }).then(res => res.data),
};

export const usersApi = {
  getUsers: () => api.post<User[]>('/api/users/get_users').then(res => res.data),
  createUser: (user: { username: string; password: string }) => 
    api.post<User>('/api/users/create_user', user).then(res => res.data),
  updateUser: (user: { id: number } & Partial<User>) => 
    api.post<User>('/api/users/update_user', user).then(res => res.data),
  deleteUser: (id: number) => api.post('/api/users/delete_user', { id }).then(res => res.data),
};

export const weatherApi = {
  getWeatherInfo: () => {
    const token = localStorage.getItem('token');
    return api.post<{ response: { code: number; message: string }; result: { data: WeatherInfo[] } }>(
      '/api/weather_info/get_weather_info',
      { access_token: token }
    ).then(res => res.data.result.data);
  },
  createWeatherInfo: (info: { lat: number; lon: number }) => {
    const token = localStorage.getItem('token');
    return api.post<WeatherInfo>('/api/weather_info/create_weather_info', {
      ...info,
      access_token: token
    }).then(res => res.data);
  },
  updateWeatherInfo: (id: number) => {
    const token = localStorage.getItem('token');
    return api.post<WeatherInfo>('/api/weather_info/update_weather_info', {
      id,
      access_token: token
    }).then(res => res.data);
  }
};

export const authApi = {
  login: (username: string, password: string) => {
    return api.post<{ access_token: string }>('/login', null, {  // Changed back to /login and null payload
      auth: {  // Use axios auth option instead of manual Basic Auth header
        username,
        password
      }
    }).then(res => res.data);
  }
};

// Add interceptor to handle 401 responses
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;