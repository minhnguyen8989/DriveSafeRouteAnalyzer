import os

import requests

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

from services.mapbox_service import (
    geocode,
    get_route
)

from services.weather_service import (
    get_weather
)

from services.route_utils import (
    sample_route_coordinates
)

from safety.safety_analyzer import (
    analyze_weather
)


# Load environment variables from .env
load_dotenv()


def create_app(test_config=None):
    """
    Flask application factory.

    test_config allows pytest to provide fake API keys
    without using real credentials.
    """

    app = Flask(__name__)

    # --------------------------------------------------
    # Application configuration
    # --------------------------------------------------

    app.config.from_mapping(
        MAPBOX_SERVER_TOKEN=os.getenv(
            "MAPBOX_SERVER_TOKEN"
        ),
        OPENWEATHER_API_KEY=os.getenv(
            "OPENWEATHER_API_KEY"
        )
    )

    # Override configuration during testing
    if test_config:
        app.config.update(test_config)

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------

    @app.get("/")
    def home():
        return render_template(
            "index.html"
        )

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok"
        })

    # --------------------------------------------------
    # Analyze Route API
    # --------------------------------------------------

    @app.post("/api/analyze-route")
    def analyze_route_endpoint():

        # ----------------------------------------------
        # Read JSON request
        # ----------------------------------------------

        data = request.get_json(
            silent=True
        ) or {}

        start_address = (
            data.get("start", "")
            .strip()
        )

        destination_address = (
            data.get("destination", "")
            .strip()
        )

        # ----------------------------------------------
        # Validate input
        # ----------------------------------------------

        if not start_address:
            return jsonify({
                "error":
                    "Starting location is required."
            }), 400

        if not destination_address:
            return jsonify({
                "error":
                    "Destination is required."
            }), 400

        # ----------------------------------------------
        # Retrieve API credentials
        # ----------------------------------------------

        mapbox_token = app.config.get(
            "MAPBOX_SERVER_TOKEN"
        )

        weather_key = app.config.get(
            "OPENWEATHER_API_KEY"
        )

        try:

            # ==========================================
            # STEP 1:
            # Geocode starting location
            # ==========================================

            start = geocode(
                address=start_address,
                token=mapbox_token
            )

            # ==========================================
            # STEP 2:
            # Geocode destination
            # ==========================================

            destination = geocode(
                address=destination_address,
                token=mapbox_token
            )

            # ==========================================
            # STEP 3:
            # Get route from Mapbox
            # ==========================================

            route = get_route(
                start_longitude=start[
                    "longitude"
                ],
                start_latitude=start[
                    "latitude"
                ],
                end_longitude=destination[
                    "longitude"
                ],
                end_latitude=destination[
                    "latitude"
                ],
                token=mapbox_token
            )

            # ==========================================
            # STEP 4:
            # Extract route coordinates
            # ==========================================

            route_coordinates = (
                route[
                    "geometry"
                ][
                    "coordinates"
                ]
            )

            # ==========================================
            # STEP 5:
            # Sample route coordinates
            #
            # We do not call OpenWeather for every
            # Mapbox coordinate.
            #
            # For now:
            #     Start
            #     Middle
            #     Destination
            # ==========================================

            sampled_coordinates = (
                sample_route_coordinates(
                    route_coordinates,
                    max_points=3
                )
            )

            # ==========================================
            # STEP 6:
            # Retrieve weather and perform
            # safety analysis
            # ==========================================

            weather_points = []

            for longitude, latitude in (
                sampled_coordinates
            ):

                weather = get_weather(
                    latitude=latitude,
                    longitude=longitude,
                    api_key=weather_key
                )

                safety = analyze_weather(
                    weather
                )

                weather_points.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "weather": weather,
                    "safety": safety
                })

            # ==========================================
            # STEP 7:
            # Determine highest risk along route
            # ==========================================

            risk_order = {
                "LOW": 0,
                "MODERATE": 1,
                "HIGH": 2
            }

            overall_risk = "LOW"

            for point in weather_points:

                point_risk = (
                    point[
                        "safety"
                    ][
                        "risk_level"
                    ]
                )

                if (
                    risk_order[point_risk]
                    >
                    risk_order[overall_risk]
                ):
                    overall_risk = point_risk

            # ==========================================
            # STEP 8:
            # Return final API response
            # ==========================================

            return jsonify({
                "start": start,

                "destination": destination,

                "route": {
                    "distance":
                        route["distance"],

                    "duration":
                        route["duration"],

                    "geometry":
                        route["geometry"]
                },

                "weather_points":
                    weather_points,

                "overall_risk":
                    overall_risk
            }), 200

        # --------------------------------------------------
        # External API timeout
        # --------------------------------------------------

        except requests.exceptions.Timeout:

            return jsonify({
                "error":
                    "External API request timed out."
            }), 504

        # --------------------------------------------------
        # External API HTTP/network failure
        #
        # Examples:
        # 401 Unauthorized
        # 429 Too Many Requests
        # 500 Server Error
        # Network connection failure
        # --------------------------------------------------

        except requests.exceptions.RequestException:

            return jsonify({
                "error":
                    "External API request failed."
            }), 502

        # --------------------------------------------------
        # Application/data errors
        #
        # Examples:
        # Mapbox location not found
        # Mapbox route not found
        # --------------------------------------------------

        except ValueError as error:

            return jsonify({
                "error": str(error)
            }), 400

    return app


# ------------------------------------------------------
# Local Development Server
# ------------------------------------------------------

if __name__ == "__main__":

    app = create_app()

    app.run(
        debug=True
    )