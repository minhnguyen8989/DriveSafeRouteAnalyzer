import requests


OPENWEATHER_CURRENT_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


def get_weather(
    latitude,
    longitude,
    api_key
):
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "imperial"
    }

    response = requests.get(
        OPENWEATHER_CURRENT_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather = data["weather"][0]

    return {
        "temperature": data["main"]["temp"],
        "condition": weather["main"],
        "description": weather["description"],
        "wind_speed": data["wind"]["speed"],
        "visibility": data.get("visibility"),
        "humidity": data["main"]["humidity"]
    }