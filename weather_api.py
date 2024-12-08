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
        #location_info = data['location']
        # Print the current weather information
        # print(f"Current weather in {location_info['name']}, {location_info['region']}, {location_info['country']}:")
        # print(f"Temperature: {current_weather['temp_c']}°C / {current_weather['temp_f']}°F")
        # print(f"Condition: {current_weather['condition']['text']}")
        # print(f"Humidity: {current_weather['humidity']}%")
        # print(f"Wind Speed: {current_weather['wind_kph']} km/h / {current_weather['wind_mph']} mph")
        # print(f"Last Updated: {current_weather['last_updated']}")
        return current_weather['temp_c'], current_weather['condition']['text'], current_weather['humidity'], current_weather['wind_kph']
    else:
        #print(f"Error: Unable to fetch weather data. Status Code: {response.status_code}")
        return None
