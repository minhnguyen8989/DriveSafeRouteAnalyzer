from services.mapbox_service import (
    MAPBOX_GEOCODING_URL,
    MAPBOX_DIRECTIONS_BASE_URL
)

from services.weather_service import (
    OPENWEATHER_CURRENT_URL
)


def test_analyze_route(
    client,
    requests_mock
):

    # -----------------------------
    # Mock Mapbox geocoding calls
    # -----------------------------

    houston_response = {
        "type": "FeatureCollection",

        "features": [
            {
                "type": "Feature",

                "geometry": {
                    "type": "Point",

                    "coordinates": [
                        -95.3698,
                        29.7604
                    ]
                }
            }
        ]
    }

    austin_response = {
        "type": "FeatureCollection",

        "features": [
            {
                "type": "Feature",

                "geometry": {
                    "type": "Point",

                    "coordinates": [
                        -97.7431,
                        30.2672
                    ]
                }
            }
        ]
    }

    requests_mock.get(
        MAPBOX_GEOCODING_URL,
        [
            {
                "json": houston_response,
                "status_code": 200
            },

            {
                "json": austin_response,
                "status_code": 200
            }
        ]
    )

    # -----------------------------
    # Mock Mapbox Directions
    # -----------------------------

    directions_url = (
        f"{MAPBOX_DIRECTIONS_BASE_URL}/driving/"
        "-95.3698,29.7604;"
        "-97.7431,30.2672"
    )

    route_response = {
        "routes": [
            {
                "distance": 265000.0,

                "duration": 9300.0,

                "geometry": {
                    "type": "LineString",

                    "coordinates": [
                        [-95.3698, 29.7604],
                        [-95.8000, 29.8500],
                        [-96.5000, 30.0000],
                        [-97.0000, 30.1000],
                        [-97.7431, 30.2672]
                    ]
                }
            }
        ]
    }

    requests_mock.get(
        directions_url,
        json=route_response,
        status_code=200
    )

    # -----------------------------
    # Mock OpenWeather calls
    # -----------------------------

    clear_weather = {
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],

        "main": {
            "temp": 75,
            "humidity": 50
        },

        "wind": {
            "speed": 5
        },

        "visibility": 10000
    }

    rain_weather = {
        "weather": [
            {
                "main": "Rain",
                "description": "moderate rain"
            }
        ],

        "main": {
            "temp": 68,
            "humidity": 85
        },

        "wind": {
            "speed": 12
        },

        "visibility": 6000
    }

    storm_weather = {
        "weather": [
            {
                "main": "Thunderstorm",
                "description": "heavy thunderstorm"
            }
        ],

        "main": {
            "temp": 66,
            "humidity": 92
        },

        "wind": {
            "speed": 35
        },

        "visibility": 2000
    }

    requests_mock.get(
        OPENWEATHER_CURRENT_URL,
        [
            {
                "json": clear_weather,
                "status_code": 200
            },

            {
                "json": rain_weather,
                "status_code": 200
            },

            {
                "json": storm_weather,
                "status_code": 200
            }
        ]
    )

    # -----------------------------
    # Call our Flask API
    # -----------------------------

    response = client.post(
        "/api/analyze-route",

        json={
            "start": "Houston, TX",
            "destination": "Austin, TX"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["route"]["distance"] == 265000.0

    assert data["route"]["duration"] == 9300.0

    assert len(
        data["weather_points"]
    ) == 3

    assert data["overall_risk"] == "HIGH"