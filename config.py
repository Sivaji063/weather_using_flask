import os
from dotenv import load_dotenv
load_dotenv()
class Config:
	OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
	OPENWEATHER_BASE_URL = os.getenv(
		"OPENWEATHER_BASE_URL",
		"https://api.openweathermap.org/data/2.5",
	)
	REQUEST_TIMEOUT = 10
	DEFAULT_UNITS = "metric"
if not Config.OPENWEATHER_API_KEY:
	raise ValueError("OPENWEATHER_API_KEY not set in .env")
