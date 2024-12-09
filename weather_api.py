import requests
# API_KEY = "c2d5c03c8cb24864968192327240812"

def getCurrWeather(loc):
    API_KEY = "c2d5c03c8cb24864968192327240812"
    location = loc
    # Construct the API URL
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_weather = data['current']

        return current_weather['temp_c'], current_weather['condition']['text'], current_weather['humidity'], current_weather['wind_kph']
    else:
        #print(f"Error: Unable to fetch weather data. Status Code: {response.status_code}")
        return None