const weatherForm = document.querySelector(".weatherForm");
const cityInput = document.querySelector(".cityInput");
const card = document.querySelector(".card");
const statusMessage = document.querySelector(".statusMessage");
const submitButton = weatherForm.querySelector('button[type="submit"]');

/*
    API key handling:
    For this simple frontend project, use your own OpenWeatherMap API key.

    Do not commit a real key to a public GitHub repository.
    See README.md for setup instructions.
*/
const apiKey = "YOUR_OPENWEATHERMAP_API_KEY";

const weatherClasses = [
    "thunderstorm",
    "drizzle",
    "rain",
    "snow",
    "mist",
    "clear",
    "clouds"
];

weatherForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const city = cityInput.value.trim();

    if (!city) {
        displayError("Please enter a city name.");
        return;
    }

    if (apiKey === "YOUR_OPENWEATHERMAP_API_KEY") {
        displayError("Add your OpenWeatherMap API key in script.js before searching.");
        return;
    }

    setLoading(true);

    try {
        const weatherData = await getWeatherData(city);
        displayWeatherInfo(weatherData);
    } catch (error) {
        console.error(error);
        displayError(error.message);
    } finally {
        setLoading(false);
    }
});

async function getWeatherData(city) {
    const apiUrl =
        `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}`;

    const response = await fetch(apiUrl);

    if (response.status === 404) {
        throw new Error(`Could not find "${city}". Check the spelling and try again.`);
    }

    if (response.status === 401) {
        throw new Error("The API key is invalid or not configured.");
    }

    if (!response.ok) {
        throw new Error("Could not fetch weather data. Please try again.");
    }

    return await response.json();
}

function displayWeatherInfo(data) {
    const {
        name: city,
        main: { temp, humidity },
        weather: [{ description, id }]
    } = data;

    changeBackground(id);

    card.textContent = "";
    card.hidden = false;

    const cityDisplay = document.createElement("h1");
    const tempDisplay = document.createElement("p");
    const humidityDisplay = document.createElement("p");
    const descDisplay = document.createElement("p");
    const weatherEmoji = document.createElement("p");

    cityDisplay.textContent = city;
    tempDisplay.textContent = `${(temp - 273.15).toFixed(1)}°C`;
    humidityDisplay.textContent = `Humidity: ${humidity}%`;
    descDisplay.textContent = description;
    weatherEmoji.textContent = getWeatherEmoji(id);

    cityDisplay.classList.add("cityDisplay");
    tempDisplay.classList.add("tempDisplay");
    humidityDisplay.classList.add("humidityDisplay");
    descDisplay.classList.add("descDisplay");
    weatherEmoji.classList.add("weatherEmoji");

    card.append(
        cityDisplay,
        tempDisplay,
        humidityDisplay,
        descDisplay,
        weatherEmoji
    );

    statusMessage.textContent = "";
}

function getWeatherEmoji(weatherId) {
    switch (true) {
        case weatherId >= 200 && weatherId < 300:
            return "⛈️";

        case weatherId >= 300 && weatherId < 400:
            return "🌧️";

        case weatherId >= 500 && weatherId < 600:
            return "🌧️";

        case weatherId >= 600 && weatherId < 700:
            return "❄️";

        case weatherId >= 700 && weatherId < 800:
            return "🌫️";

        case weatherId === 800:
            return "☀️";

        case weatherId >= 801 && weatherId < 810:
            return "☁️";

        default:
            return "❓";
    }
}

function changeBackground(weatherId) {
    document.body.classList.remove(...weatherClasses);

    switch (true) {
        case weatherId >= 200 && weatherId < 300:
            document.body.classList.add("thunderstorm");
            break;

        case weatherId >= 300 && weatherId < 400:
            document.body.classList.add("drizzle");
            break;

        case weatherId >= 500 && weatherId < 600:
            document.body.classList.add("rain");
            break;

        case weatherId >= 600 && weatherId < 700:
            document.body.classList.add("snow");
            break;

        case weatherId >= 700 && weatherId < 800:
            document.body.classList.add("mist");
            break;

        case weatherId === 800:
            document.body.classList.add("clear");
            break;

        case weatherId >= 801 && weatherId < 810:
            document.body.classList.add("clouds");
            break;
    }
}

function displayError(message) {
    card.textContent = "";

    const errorDisplay = document.createElement("p");
    errorDisplay.textContent = message;
    errorDisplay.classList.add("errorDisplay");

    card.appendChild(errorDisplay);
    card.hidden = false;

    statusMessage.textContent = "";
}

function setLoading(isLoading) {
    submitButton.disabled = isLoading;

    if (isLoading) {
        statusMessage.textContent = "Loading weather...";
        card.hidden = true;
    } else {
        statusMessage.textContent = "";
    }
}
