import { Box, Typography } from '@mui/material';

export default function Home() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to OpenWeather Webapp
      </Typography>
      <Typography variant="body1">
        Use the sidebar to navigate through different sections to view weather information.
      </Typography>
    </Box>
  );
} 