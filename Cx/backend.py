import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
#---------------------------------------------------------------------------------------------

weather_codes = {
    "0": "Cloud development not observed or observable",
    "1": "Clouds dissolving or becoming less developed",
    "2": "State of sky on the whole unchanged",
    "3": "Clouds generally forming or developing",
    "4": "Visibility reduced by smoke haze",
    "5": "Haze",
    "6": "Widespread dust in suspension in the air, not raised by wind at or near the station at the time of observation",
    "7": "Dust or sand raised by the wind at or near the station at the time of the observation, but no well-developed dust whirl(s), and no sandstorm seen: or, in the case of ships, blowing spray at the station",
    "8": "Well developed dust whirl(s) or sand whirl(s) seen at or near the station during the preceding hour or at the time of observation, but no duststorm or sandstorm",
    "9": "Duststorm or sandstorm within sight at the time of observation, or at the station during the preceding hour",
    "10": "Mist",
    "11": "Patches of shallow fog or ice fog",
    "12": "More or less continuous",
    "13": "Lightning visible, no thunder heard",
    "14": "Precipitation within sight, not reaching the ground or surface of sea",
    "15": "Precipitation within sight, reaching ground or the surface of the sea, but distant, i.e. estimated to be more than 5 km from the station",
    "16": "Precipitation within sight, reaching the ground or the surface of the sea, near to, but not at the station",
    "17": "Thunderstorm, but no precipitation at the time of observation",
    "18": "Squalls at or within sight of the station during",
    "19": "Funnel cloud(s) or tuba during the preceding hour or at time of observation",
    "20": "Drizzle (not freezing) or snow grains",
    "21": "Rain (not freezing)",
    "22": "Snow",
    "23": "Rain and snow or ice pellets",
    "24": "Freezing drizzle or freezing rain",
    "25": "Shower(s) of rain",
    "26": "Shower(s) of snow, or of rain and snow",
    "27": "Shower(s) of hail, or of rain and hail",
    "28": "Fog or ice fog",
    "29": "Thunderstorm (with or without precipitation)",
    "30": "Slight duststorm ( has decreased during the preceding hour )",
    "31": "Moderate duststorm ( no appreciable change during the preceding hour)",
    "32": "Sandstorm ( has begun or increased during the preceding hour)",
    "33": "Severe Sandstorm ( has decreased during the preceding hour)",
    "34": "Duststorm ( no appreciable change during the preceding hour)",
    "35": "Sandstorm ( has begun or increased during the preceding hour)",
    "36": "Slight or moderate drifting snow ( generally low)",
    "37": "Heavy drifting snow ( below eye level)",
    "38": "Slight or moderate blowing snow ( generally high)",
    "39": "Heavy blowing snow ( above eye level)",
    "40": "Fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer",
    "41": "Fog or ice fog in patches",
    "42": "Fog or ice fog, sky visible ( has become thinner during the preceding hour)",
    "43": "Fog or ice fog, sky obscured ( has become thinner during the preceding hour)",
    "44": "Fog or ice fog, sky visible ( no appreciable change)",
    "45": "Fog or ice fog, sky obscured ( during the preceding hour)",
    "46": "Fog or ice fog, sky visible ( has begun or has become thicker during the preceding hour)",
    "47": "Fog or ice fog, sky obscured ( has begun or has become thicker during the preceding hour)",
    "48": "Fog or ice fog, sky visible",
    "49": "Fog or ice fog, sky obscured",
    "50": "Drizzle, not freezing, intermittent ( slight at time of observation)",
    "51": "Drizzle, not freezing, continuous ( slight at time of observation)",
    "52": "Drizzle, not freezing, intermittent ( moderate at time of observation)",
    "53": "Drizzle, not freezing, continuous ( moderate at time of observation)",
    "54": "Drizzle, not freezing, intermittent ( heavy (dense) at time of observation)",
    "55": "Drizzle, not freezing, continuous ( heavy (dense) at time of observation)",
    "56": "Drizzle, freezing, slight",
    "57": "Drizzle, freezing, moderate or heavy (dense)",
    "58": "Drizzle and rain, slight",
    "59": "Drizzle and rain, moderate or heavy",
    "60": "Rain, not freezing, intermittent ( slight at time of observation)",
    "61": "Rain, not freezing, continuous ( slight at time of observation)",
    "62": "Rain, not freezing, intermittent ( moderate at time of observation)",
    "63": "Rain, not freezing, continuous ( moderate at time of observation)",
    "64": "Rain, not freezing, intermittent ( heavy at time of observation)",
    "65": "Rain, not freezing, continuous ( heavy at time of observation)",
    "66": "Rain, freezing, slight",
    "67": "Rain, freezing, moderate or heavy",
    "68": "Rain or drizzle and snow, slight",
    "69": "Rain or drizzle and snow, moderate or heavy",
    "70": "Intermittent fall of snowflakes ( slight at time of observation)",
    "71": "Continuous fall of snowflakes ( slight at time of observation)",
    "72": "Intermittent fall of snowflakes ( moderate at time of observation)",
    "73": "Continuous fall of snowflakes ( moderate at time of observation)",
    "74": "Intermittent fall of snowflakes( heavy at time of observation)",
    "75": "Continuous fall of snowflakes ( heavy at time of observation)",
    "76": "Diamond dust (with or without fog)",
    "77": "Snow grains (with or without fog)",
    "78": "Isolated star-like snow crystals (with or without fog)",
    "79": "Ice pellets",
    "80": "Rain shower(s), slight",
    "81": "Rain shower(s), moderate or heavy",
    "82": "Rain shower(s), violent",
    "83": "Shower(s) of rain and snow mixed, slight",
    "84": "Shower(s) of rain and snow mixed, moderate or heavy",
    "85": "Snow shower(s), slight",
    "86": "Snow shower(s), moderate or heavy",
    "87": "Shower(s) of snow pellets or small hail ( slight )...",
    "88": "...with or without rain or rain and snow mixed ( moderate or heavy)",
    "89": "Shower(s) of hail, with or without rain or( slight )...",
    "90": "...rain and snow mixed, not associated with thunder ( moderate or heavy)",
    "91": "Slight rain at time of observation",
    "92": "Moderate or heavy rain at time of observation",
    "93": "Slight snow, or rain and snow mixed, or hail (2) at time of observation",
    "94": "Moderate or heavy snow, or rain and snow mixed, or hail (1) at time of observation",
    "95": "Thunderstorm, slight or moderate, without hail (2) but with rain and or snow at time of observation",
    "96": "Thunderstorm, slight or moderate, with hail (2) at time of observation",
    "97": "Thunderstorm, heavy, without hail (2) but with rain and or snow at time of observation",
    "98": "Thunderstorm combined with duststorm or sandstorm at time of observation",
    "99": "Thunderstorm, heavy, with hail (2) at time of observation"
}


#---------------------------------------------------------------------------------------------
def get_historical_weather(latitude,longitude):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"start_date": "2024-04-12",
		"end_date": "2024-04-26",
		"daily": ["weather_code", "temperature_2m_mean", "rain_sum"]
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	# daily_weather_code =  [weather_codes[code] for code in daily.Variables(0)].ValuesAsNumpy()
	daily_weather_code = [weather_codes[str(int(code))] for code in daily.Variables(0).ValuesAsNumpy()]
	daily_temperature_2m_mean = daily.Variables(1).ValuesAsNumpy()
	daily_rain_sum = daily.Variables(2).ValuesAsNumpy()
	print(type(daily.Variables(0)))
	daily_data = {"Date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["Weather Code"] = daily_weather_code
	daily_data["Mean Temperature"] = daily_temperature_2m_mean
	daily_data["Rain Sum"] = daily_rain_sum	
	print(type(daily_weather_code))
	daily_dataframe = pd.DataFrame(data = daily_data)
	return daily_dataframe



api_key='cd2f130bbd95a330d9edb40d200f98a8'
def get_weather_data(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None
    

def get_forecast(lat,lon):
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": lat,
		"longitude": lon,
		"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "rain_sum"],
		"timezone": "Asia/Singapore"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	# daily_weather_code = daily.Variables(0).ValuesAsNumpy()
	daily_weather_code = [str("Should be : "+weather_codes[str(int(code))]) for code in daily.Variables(0).ValuesAsNumpy()]
	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_rain_sum = daily.Variables(3).ValuesAsNumpy()

	daily_data = {"Date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["Weather Code"] = daily_weather_code
	daily_data["Max Temperature"] = daily_temperature_2m_max
	daily_data["Min Temperature"] = daily_temperature_2m_min
	daily_data["Rain Sum"] = daily_rain_sum

	daily_dataframe = pd.DataFrame(data = daily_data)
	return daily_dataframe