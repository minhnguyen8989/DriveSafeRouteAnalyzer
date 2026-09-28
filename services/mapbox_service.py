import requests


MAPBOX_GEOCODING_URL = (
    "https://api.mapbox.com/search/geocode/v6/forward"
)


def geocode(address, token):

    params = {
        "q": address,
        "access_token": token,
        "limit": 1
    }

    response = requests.get(
        MAPBOX_GEOCODING_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    features = data.get("features", [])

    if not features:
        raise ValueError("Location not found")

    feature = features[0]

    longitude, latitude = (
        feature["geometry"]["coordinates"]
    )

    return {
        "latitude": latitude,
        "longitude": longitude
    }