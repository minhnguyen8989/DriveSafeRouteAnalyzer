from services.weather_service import (
    OPENWEATHER_CURRENT_URL,
    get_weather
)


def test_get_weather_returns_weather_data(
    requests_mock
):
    fake_response = {
        "coord": {
            "lon": -95.3698,
            "lat": 29.7604
        },

        "weather": [
            {
                "id": 500,
                "main": "Rain",
                "description": "light rain",
                "icon": "10d"
            }
        ],

        "main": {
            "temp": 72.5,
            "feels_like": 73.1,
            "pressure": 1012,
            "humidity": 85
        },

        "visibility": 5000,

        "wind": {
            "speed": 18.2,
            "deg": 180
        },

        "name": "Houston"
    }

    requests_mock.get(
        OPENWEATHER_CURRENT_URL,
        json=fake_response,
        status_code=200
    )

    result = get_weather(
        latitude=29.7604,
        longitude=-95.3698,
        api_key="fake-openweather-key"
    )

    assert result["temperature"] == 72.5
    assert result["condition"] == "Rain"
    assert result["description"] == "light rain"
    assert result["wind_speed"] == 18.2
    assert result["visibility"] == 5000
    assert result["humidity"] == 85

def test_get_weather_sends_correct_parameters(
    requests_mock
):
    fake_response = {
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],

        "main": {
            "temp": 80,
            "humidity": 55
        },

        "wind": {
            "speed": 5
        },

        "visibility": 10000
    }

    requests_mock.get(
        OPENWEATHER_CURRENT_URL,
        json=fake_response,
        status_code=200
    )

    get_weather(
        latitude=29.7604,
        longitude=-95.3698,
        api_key="fake-openweather-key"
    )

    request = requests_mock.last_request

    assert request.method == "GET"

    assert request.qs["lat"] == [
        "29.7604"
    ]

    assert request.qs["lon"] == [
        "-95.3698"
    ]

    assert request.qs["appid"] == [
        "fake-openweather-key"
    ]

    assert request.qs["units"] == [
        "imperial"
    ]