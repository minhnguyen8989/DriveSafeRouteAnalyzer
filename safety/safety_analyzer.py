def analyze_weather(weather):

    score = 0
    warnings = []

    condition = weather["condition"].lower()

    if "rain" in condition:
        score += 20
        warnings.append("Rain detected")

    if "thunderstorm" in condition:
        score += 50
        warnings.append("Thunderstorm detected")

    if weather["wind_speed"] >= 30:
        score += 25
        warnings.append("Strong wind detected")

    if weather["temperature"] <= 32:
        score += 25
        warnings.append("Freezing temperature detected")

    if weather["visibility"] < 3000:
        score += 25
        warnings.append("Low visibility detected")

    if score == 0:
        risk_level = "LOW"

    elif score < 50:
        risk_level = "MODERATE"

    else:
        risk_level = "HIGH"

    return {
        "score": score,
        "risk_level": risk_level,
        "warnings": warnings
    }