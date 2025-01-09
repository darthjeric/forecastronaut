from flask import Flask, render_template, request
import requests
from config import API_KEY
import os

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API key
#OPENWEATHERMAP_API_KEY = API_KEY
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    country_code = request.form.get('country_code', '')

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPENWEATHERMAP_API_KEY}"

    try:
        response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenWeatherMap API: {e}")
        return render_template('error.html', error="Error fetching weather data.")

    if response:
        if response['cod'] == 200:
            temperature_kelvin = response['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            weather = {
                'city': city,
                'temperature': f"{temperature_celsius:.2f}",  # Format temperature to 2 decimal places
                'description': response['weather'][0]['description']
            }
            print(f"Temperature in {city}, {country_code}: {weather['temperature']} °C")
            print(f"Weather description: {weather['description']}")
            return render_template('weather.html', **weather)  # Pass data as keyword arguments
        else:
            print(f"Error: {response['message']}")
            return render_template('error.html', error=error)
    else:
        print("No results found for the specified city.")
        return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)