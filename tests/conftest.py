import pytest

from app import create_app


@pytest.fixture()
def app():

    app = create_app({
        "TESTING": True,

        "MAPBOX_SERVER_TOKEN":
            "fake-mapbox-token",

        "OPENWEATHER_API_KEY":
            "fake-openweather-key"
    })

    yield app