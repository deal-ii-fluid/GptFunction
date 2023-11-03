import requests
import json
def get_current_weather(location, unit='metric'):
    # OpenWeatherMap API endpoint
    # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    api_key = '9406b031866f08b6e1da394ce216aa6a'


    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={unit}"

    # Send request
    response = requests.get(url)
    data = response.json()

    # Check for errors
    if response.status_code != 200:
        print(f"Failed to get data: {data['message']}")
        return None

    # Parse and print the weather data
    weather = {
        "location": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"],
    }

    return weather

