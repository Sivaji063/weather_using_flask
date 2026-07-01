from dataclasses import dataclass

import requests

from config import Config


@dataclass
class WeatherData:
	city: str
	temperature: float
	feels_like: float
	humidity: int
	description: str
	icon: str
	wind_speed: float
	pressure: int


class WeatherError(Exception):
	pass


class WeatherService:
	def __init__(self):
		self.api_key = Config.OPENWEATHER_API_KEY
		self.base_url = Config.OPENWEATHER_BASE_URL
		self.timeout = Config.REQUEST_TIMEOUT
		self.default_units = Config.DEFAULT_UNITS

	def _make_request(self, endpoint: str, params: dict) -> dict:
		params["appid"] = self.api_key
		params["units"] = self.default_units

		url = f"{self.base_url}/{endpoint}"

		try:
			response = requests.get(url, params=params, timeout=self.timeout)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.Timeout:
			raise WeatherError("Request timed out. Please try again.")
		except requests.exceptions.HTTPError as e:
			if response.status_code == 401:
				raise WeatherError("Invalid API key. Check your OpenWeather configuration.")
			if response.status_code == 404:
				raise WeatherError("City not found. Please check the spelling.")
			if response.status_code == 429:
				raise WeatherError("Rate limit exceeded. Please wait a moment.")
			raise WeatherError(f"API error: {str(e)}")
		except requests.exceptions.RequestException as e:
			raise WeatherError(f"Network error: {str(e)}")

	def get_current_weather(self, city: str) -> WeatherData:
		data = self._make_request("weather", {"q": city})

		return WeatherData(
			city=data["name"],
			temperature=round(data["main"]["temp"], 1),
			feels_like=round(data["main"]["feels_like"], 1),
			humidity=data["main"]["humidity"],
			description=data["weather"][0]["description"].capitalize(),
			icon=data["weather"][0]["icon"],
			wind_speed=data["wind"]["speed"],
			pressure=data["main"]["pressure"],
		)

	def get_forecast(self, city: str, days: int = 5) -> list:
		data = self._make_request("forecast", {"q": city, "cnt": days * 8})

		forecasts = []
		for item in data["list"]:
			forecasts.append(
				{
					"datetime": item["dt_txt"],
					"temperature": round(item["main"]["temp"], 1),
					"description": item["weather"][0]["description"].capitalize(),
					"icon": item["weather"][0]["icon"],
					"humidity": item["main"]["humidity"],
					"wind_speed": item["wind"]["speed"],
				}
			)
		return forecasts
