import os

from dotenv import load_dotenv

from flask import (
    Flask,
    jsonify,
    request
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


load_dotenv()


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_mapping(
        MAPBOX_SERVER_TOKEN=os.getenv(
            "MAPBOX_SERVER_TOKEN"
        ),

        OPENWEATHER_API_KEY=os.getenv(
            "OPENWEATHER_API_KEY"
        )
    )

    if test_config:
        app.config.update(test_config)

    @app.get("/health")
    def health():

        return jsonify({
            "status": "ok"
        })

    @app.post("/api/analyze-route")
    def analyze_route_endpoint():

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

        mapbox_token = app.config[
            "MAPBOX_SERVER_TOKEN"
        ]

        weather_key = app.config[
            "OPENWEATHER_API_KEY"
        ]

        # --------------------------------
        # Geocode starting location
        # --------------------------------

        start = geocode(
            start_address,
            mapbox_token
        )

        # --------------------------------
        # Geocode destination
        # --------------------------------

        destination = geocode(
            destination_address,
            mapbox_token
        )

        # --------------------------------
        # Get driving route
        # --------------------------------

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

        # --------------------------------
        # Sample route coordinates
        # --------------------------------

        route_coordinates = (
            route[
                "geometry"
            ][
                "coordinates"
            ]
        )

        sampled_coordinates = (
            sample_route_coordinates(
                route_coordinates,
                max_points=3
            )
        )

        weather_points = []

        # --------------------------------
        # Analyze weather for each point
        # --------------------------------

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

        # --------------------------------
        # Determine highest route risk
        # --------------------------------

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

        # --------------------------------
        # Return final result
        # --------------------------------

        return jsonify({
            "start": start,

            "destination":
                destination,

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
        })

    return app


if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)