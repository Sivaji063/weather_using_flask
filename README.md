# Weather App

A simple Flask web app that shows current weather and a 5-day forecast for any city, using the OpenWeatherMap API.

## Features
- Search current weather by city name
- Displays temperature, feels-like, humidity, wind speed, pressure, and conditions
- 5-day forecast grouped by day
- Clean, responsive single-page UI

## Project Structure
```
weather-app/
├── app.py                 # Flask routes
├── config.py               # App configuration, loads .env
├── services/
│   └── weather.py          # OpenWeatherMap API client
├── templates/
│   └── index.html          # Frontend UI
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

1. Clone the repo
   ```bash
   git clone <your-repo-url>
   cd weather-app
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Get an API key from [OpenWeatherMap](https://openweathermap.org/api) (free tier works).

4. Create a `.env` file in the project root (copy `.env.example`) and add your key:
   ```
   OPENWEATHER_API_KEY=your_actual_key_here
   OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
   FLASK_ENV=development
   ```

5. Run the app
   ```bash
   python app.py
   ```

6. Open [http://localhost:5000](http://localhost:5000) in your browser.

## API Endpoints
- `GET /api/weather?city=<city>` — current weather
- `GET /api/forecast?city=<city>` — 5-day forecast

## Notes
- Never commit your real `.env` file — it's excluded via `.gitignore`.
- If a real API key was ever exposed publicly, regenerate it from your OpenWeatherMap account settings.

## License
MIT
