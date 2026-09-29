from safety.safety_analyzer import analyze_weather


def test_clear_weather_returns_low_risk():

    weather = {
        "temperature": 75,
        "condition": "Clear",
        "description": "clear sky",
        "wind_speed": 5,
        "visibility": 10000,
        "humidity": 50
    }

    result = analyze_weather(weather)

    assert result["score"] == 0
    assert result["risk_level"] == "LOW"
    assert result["warnings"] == []

def test_rain_increases_risk():

    weather = {
        "temperature": 68,
        "condition": "Rain",
        "description": "moderate rain",
        "wind_speed": 10,
        "visibility": 8000,
        "humidity": 80
    }

    result = analyze_weather(weather)

    assert result["score"] >= 20

    assert result["risk_level"] == "MODERATE"

    assert "Rain detected" in result["warnings"]

def test_thunderstorm_returns_high_risk():

    weather = {
        "temperature": 70,
        "condition": "Thunderstorm",
        "description": "heavy thunderstorm",
        "wind_speed": 15,
        "visibility": 6000,
        "humidity": 90
    }

    result = analyze_weather(weather)

    assert result["score"] >= 50

    assert result["risk_level"] == "HIGH"

    assert "Thunderstorm detected" in result["warnings"]

def test_high_wind_adds_warning():

    weather = {
        "temperature": 72,
        "condition": "Clear",
        "description": "clear sky",
        "wind_speed": 35,
        "visibility": 10000,
        "humidity": 45
    }

    result = analyze_weather(weather)

    assert result["score"] >= 25

    assert "Strong wind detected" in result["warnings"]

def test_low_visibility_adds_warning():

    weather = {
        "temperature": 65,
        "condition": "Mist",
        "description": "mist",
        "wind_speed": 5,
        "visibility": 2000,
        "humidity": 95
    }

    result = analyze_weather(weather)

    assert result["score"] >= 25

    assert "Low visibility detected" in result["warnings"]

def test_freezing_temperature_adds_warning():

    weather = {
        "temperature": 28,
        "condition": "Clear",
        "description": "clear sky",
        "wind_speed": 5,
        "visibility": 10000,
        "humidity": 60
    }

    result = analyze_weather(weather)

    assert result["score"] >= 25

    assert "Freezing temperature detected" in result["warnings"]