// src/types/api.ts
export enum TaskStatus {
  Pending = "Pending",
  Completed = "Completed"
}

export interface User {
  id: number;
  username: string;
  role?: string;
  created_at?: string;
  updated_at?: string;
  is_deleted?: boolean;
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  due_date?: string;
  status: TaskStatus;
  is_deleted?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface WeatherInfo {
  id: number;
  lat: number;
  lon: number;
  timestamp: number | null;
  timezone: string;
  sunrise: number | null;
  sunset: number | null;
  temp: number | null;
  feels_like: number | null;
  pressure: number | null;
  humidity: number | null;
  dew_point: number | null;
  uvi: number | null;
  clouds: number | null;
  visibility: number | null;
  wind_speed: number | null;
  wind_deg: number | null;
  wind_gust: number | null;
  weather: string | null;
  pop: number | null;
}