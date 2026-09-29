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