from services.mapbox_service import (
    MAPBOX_GEOCODING_URL,
    geocode
)


def test_geocode_returns_coordinates(requests_mock):

    fake_response = {
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

    requests_mock.get(
        MAPBOX_GEOCODING_URL,
        json=fake_response,
        status_code=200
    )

    result = geocode(
        address="Houston, TX",
        token="fake-mapbox-token"
    )

    assert result["latitude"] == 29.7604
    assert result["longitude"] == -95.3698