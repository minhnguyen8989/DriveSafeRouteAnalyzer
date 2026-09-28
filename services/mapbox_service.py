import requests


MAPBOX_GEOCODING_URL = (
    "https://api.mapbox.com/search/geocode/v6/forward"
)

MAPBOX_DIRECTIONS_BASE_URL = (
    "https://api.mapbox.com/directions/v5/mapbox"
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


def get_route(
    start_longitude,
    start_latitude,
    end_longitude,
    end_latitude,
    token,
    profile="driving"
):

    coordinates = (
        f"{start_longitude},{start_latitude};"
        f"{end_longitude},{end_latitude}"
    )

    url = (
        f"{MAPBOX_DIRECTIONS_BASE_URL}/"
        f"{profile}/{coordinates}"
    )

    params = {
        "access_token": token,
        "geometries": "geojson",
        "overview": "full"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    routes = data.get("routes", [])

    if not routes:
        raise ValueError("Route not found")

    route = routes[0]

    return {
        "distance": route["distance"],
        "duration": route["duration"],
        "geometry": route["geometry"]
    }