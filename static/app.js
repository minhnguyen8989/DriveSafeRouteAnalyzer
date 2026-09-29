mapboxgl.accessToken =
    window.MAPBOX_PUBLIC_TOKEN;


const map = new mapboxgl.Map({
    container: "map",

    style: "mapbox://styles/mapbox/standard",

    center: [
        -98.5795,
        39.8283
    ],

    zoom: 3
});

let mapLoaded = false;

map.on(
    "load",
    () => {
        mapLoaded = true;
    }
);

map.addControl(
    new mapboxgl.NavigationControl()
);

let startMarker = null;
let destinationMarker = null;

const form =
    document.getElementById("route-form");

const analyzeButton =
    document.getElementById("analyze-button");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("error");

const results =
    document.getElementById("results");


form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        clearPageState();

        const start =
            document.getElementById(
                "start"
            ).value.trim();

        const destination =
            document.getElementById(
                "destination"
            ).value.trim();


        loading.classList.remove(
            "hidden"
        );

        analyzeButton.disabled = true;


        try {

            const response = await fetch(
                "/api/analyze-route",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        start: start,
                        destination: destination
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Route analysis failed."
                );

            }


            displayResults(data);


        } catch (error) {

            errorBox.textContent =
                error.message;

        } finally {

            loading.classList.add(
                "hidden"
            );

            analyzeButton.disabled =
                false;

        }

    }
);


function clearPageState() {

    errorBox.textContent = "";

    results.classList.add(
        "hidden"
    );

}


function displayResults(data) {

    document.getElementById(
        "overall-risk"
    ).textContent =
        data.overall_risk;


    const miles =
        metersToMiles(
            data.route.distance
        );


    const duration =
        secondsToDuration(
            data.route.duration
        );


    document.getElementById(
        "distance"
    ).textContent =
        `${miles} miles`;


    document.getElementById(
        "duration"
    ).textContent =
        duration;


    displayWeatherPoints(
        data.weather_points
    );


    results.classList.remove(
        "hidden"
    );

    map.resize();

    displayRouteOnMap(
        data
    );

}

function displayRouteOnMap(data) {

    if (!mapLoaded) {

    map.once(
        "load",
        () => {
            displayRouteOnMap(data);
        }
    );

    return;
}

    const geometry =
        data.route.geometry;

    const coordinates =
        geometry.coordinates;


    if (
        !coordinates ||
        coordinates.length === 0
    ) {
        return;
    }


    const routeGeoJSON = {
        type: "Feature",

        properties: {},

        geometry: geometry
    };


    // ---------------------------------
    // Update existing route
    // or create it the first time
    // ---------------------------------

    if (map.getSource("route")) {

        map
            .getSource("route")
            .setData(routeGeoJSON);

    } else {

        map.addSource(
            "route",
            {
                type: "geojson",
                data: routeGeoJSON
            }
        );


        map.addLayer({
            id: "route-line",

            type: "line",

            source: "route",

            layout: {
                "line-join": "round",
                "line-cap": "round"
            },

            paint: {
                "line-color": "#2563eb",
                "line-width": 6
            }
        });

    }


    // ---------------------------------
    // Remove previous markers
    // ---------------------------------

    if (startMarker) {
        startMarker.remove();
    }


    if (destinationMarker) {
        destinationMarker.remove();
    }


    // ---------------------------------
    // Start marker
    // ---------------------------------

    startMarker =
        new mapboxgl.Marker({
            color: "#16a34a"
        })
            .setLngLat(
                coordinates[0]
            )
            .addTo(map);


    // ---------------------------------
    // Destination marker
    // ---------------------------------

    destinationMarker =
        new mapboxgl.Marker({
            color: "#dc2626"
        })
            .setLngLat(
                coordinates[
                    coordinates.length - 1
                ]
            )
            .addTo(map);


    // ---------------------------------
    // Calculate route bounds
    // ---------------------------------

    const bounds =
        new mapboxgl.LngLatBounds(
            coordinates[0],
            coordinates[0]
        );


    coordinates.forEach(
        coordinate => {
            bounds.extend(
                coordinate
            );
        }
    );


    // ---------------------------------
    // Fit complete route on screen
    // ---------------------------------

    map.fitBounds(
        bounds,
        {
            padding: 50,
            duration: 1000
        }
    );

}


function displayWeatherPoints(
    weatherPoints
) {

    const container =
        document.getElementById(
            "weather-points"
        );


    container.innerHTML = "";


    weatherPoints.forEach(
        (point, index) => {

            const weather =
                point.weather;

            const safety =
                point.safety;


            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "weather-point";


            const warnings =
                safety.warnings.length > 0
                    ? safety.warnings.join(", ")
                    : "None";


            div.innerHTML = `

                <h4>
                    Route Point ${index + 1}
                </h4>

                <p>
                    <strong>Coordinates:</strong>
                    ${point.latitude.toFixed(4)},
                    ${point.longitude.toFixed(4)}
                </p>

                <p>
                    <strong>Condition:</strong>
                    ${weather.condition}
                </p>

                <p>
                    <strong>Temperature:</strong>
                    ${weather.temperature} °F
                </p>

                <p>
                    <strong>Wind:</strong>
                    ${weather.wind_speed} mph
                </p>

                <p>
                    <strong>Visibility:</strong>
                    ${weather.visibility} meters
                </p>

                <p>
                    <strong>Risk:</strong>
                    ${safety.risk_level}
                </p>

                <p>
                    <strong>Warnings:</strong>
                    ${warnings}
                </p>

            `;


            container.appendChild(
                div
            );

        }
    );

}


function metersToMiles(meters) {

    return (
        meters / 1609.344
    ).toFixed(1);

}


function secondsToDuration(seconds) {

    const totalMinutes =
        Math.round(
            seconds / 60
        );


    const hours =
        Math.floor(
            totalMinutes / 60
        );


    const minutes =
        totalMinutes % 60;


    if (hours === 0) {

        return `${minutes} min`;

    }


    return (
        `${hours} hr ${minutes} min`
    );

}