import pytest

from services.mapbox_service import (
    MAPBOX_GEOCODING_URL,
    MAPBOX_DIRECTIONS_BASE_URL,
    geocode,
    get_route
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


def test_geocode_location_not_found(requests_mock):
    fake_response = {
        "type": "FeatureCollection",
        "features": []
    }

    requests_mock.get(
        MAPBOX_GEOCODING_URL,
        json=fake_response,
        status_code=200
    )

    with pytest.raises(
        ValueError,
        match="Location not found"
    ):
        geocode(
            address="ThisPlaceDoesNotExist123",
            token="fake-mapbox-token"
        )

def test_geocode_sends_correct_request_parameters(
    requests_mock
):
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

    geocode(
        address="Houston, TX",
        token="fake-mapbox-token"
    )

    request = requests_mock.last_request

    assert request.method == "GET"

    assert request.qs["q"][0].lower() == "houston, tx"

    assert request.qs["access_token"] == [
        "fake-mapbox-token"
    ]

    assert request.qs["limit"] == [
        "1"
    ]

    assert request.qs["limit"] == [
        "1"
    ]

def test_get_route_returns_route_data(requests_mock):

    start_longitude = -95.3698
    start_latitude = 29.7604

    end_longitude = -97.7431
    end_latitude = 30.2672

    expected_url = (
        f"{MAPBOX_DIRECTIONS_BASE_URL}/driving/"
        f"{start_longitude},{start_latitude};"
        f"{end_longitude},{end_latitude}"
    )

    fake_response = {
        "routes": [
            {
                "distance": 265000.0,
                "duration": 9300.0,
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-95.3698, 29.7604],
                        [-96.0000, 29.9000],
                        [-96.5000, 30.0000],
                        [-97.0000, 30.1000],
                        [-97.7431, 30.2672]
                    ]
                }
            }
        ]
    }

    requests_mock.get(
        expected_url,
        json=fake_response,
        status_code=200
    )

    result = get_route(
        start_longitude=start_longitude,
        start_latitude=start_latitude,
        end_longitude=end_longitude,
        end_latitude=end_latitude,
        token="fake-mapbox-token"
    )

    assert result["distance"] == 265000.0
    assert result["duration"] == 9300.0

    assert result["geometry"]["type"] == "LineString"

    assert len(
        result["geometry"]["coordinates"]
    ) == 5