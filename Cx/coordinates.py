import requests

def get_coordinates(city_name):
    url = f'https://nominatim.openstreetmap.org/search?format=json&q={city_name}'
    response = requests.get(url)
    data = response.json()

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat,lon
    else:
        print("No results found.")
        return None, None