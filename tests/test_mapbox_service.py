import pytest

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