# DriveSafe Route Analyzer

DriveSafe Route Analyzer is a Python and Flask web application that combines routing and real-time weather data to identify potential weather-related driving risks along a route.

The project was built as a software engineering portfolio project to demonstrate REST API integration, backend development, JSON and GeoJSON processing, Test-Driven Development (TDD), external API mocking, error handling, and secure API credential management.

## Features

- Convert starting locations and destinations into coordinates using the Mapbox Geocoding API
- Generate driving routes using the Mapbox Directions API
- Process GeoJSON route geometry
- Sample multiple checkpoints along a route
- Retrieve current weather conditions from OpenWeather
- Analyze rain, thunderstorms, high wind, low visibility, and freezing temperatures
- Calculate a simple route risk level: `LOW`, `MODERATE`, or `HIGH`
- Display the route using Mapbox GL JS
- Display weather checkpoints directly on the map
- Handle external API errors, timeouts, invalid locations, and invalid requests
- Test external REST APIs without making real network requests

> The risk analysis in this project is an application-defined demonstration and is not an official driving-safety rating or substitute for road and weather advisories.

## Technologies

### Backend

- Python
- Flask
- Requests
- REST APIs

### APIs

- Mapbox Geocoding API
- Mapbox Directions API