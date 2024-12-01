import { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';

interface WeatherFormProps {
  onSubmit: (values: { lat: number; lon: number }) => void;
}

export default function WeatherForm({ onSubmit }: WeatherFormProps) {
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      lat: parseFloat(lat),
      lon: parseFloat(lon)
    });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          label="Latitude"
          type="number"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
          required
          inputProps={{ step: 'any' }}
        />
        <TextField
          label="Longitude"
          type="number"
          value={lon}
          onChange={(e) => setLon(e.target.value)}
          required
          inputProps={{ step: 'any' }}
        />
        <Button type="submit" variant="contained">
          Get Weather
        </Button>
      </Box>
    </Box>
  );
}