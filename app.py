from flask import Flask, jsonify, render_template, request

from config import Config
from services.weather import WeatherError, WeatherService


app = Flask(__name__)
weather_service = WeatherService()


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/api/weather", methods=["GET"])
def get_weather():
	city = request.args.get("city", "").strip()

	if not city:
		return jsonify({"error": "City parameter is required"}), 400

	try:
		weather = weather_service.get_current_weather(city)
		return jsonify(
			{
				"city": weather.city,
				"temperature": weather.temperature,
				"feels_like": weather.feels_like,
				"humidity": weather.humidity,
				"description": weather.description,
				"icon": f"https://openweathermap.org/img/wn/{weather.icon}@2x.png",
				"wind_speed": weather.wind_speed,
				"pressure": weather.pressure,
				"units": "°C" if Config.DEFAULT_UNITS == "metric" else "°F",
			}
		)
	except WeatherError as e:
		return jsonify({"error": str(e)}), 400
	except Exception as e:
		app.logger.error(f"Unexpected error: {e}")
		return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/api/forecast", methods=["GET"])
def get_forecast():
	city = request.args.get("city", "").strip()

	if not city:
		return jsonify({"error": "City parameter is required"}), 400

	try:
		forecast = weather_service.get_forecast(city)
		daily = {}
		for item in forecast:
			date = item["datetime"].split(" ")[0]
			if date not in daily:
				daily[date] = []
			daily[date].append(item)

		return jsonify({"city": city, "forecast": daily})
	except WeatherError as e:
		return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)
