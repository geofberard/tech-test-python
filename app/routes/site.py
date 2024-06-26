import copy
from flask import render_template, request, Blueprint, current_app
import requests
from app.models import Roadtrip, WeatherGuide
from app.routes.api_roadtrips import read_roadtrip_internal

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    roadtrips = Roadtrip.query.all()
    return render_template('index.html', roadtrips=roadtrips)


@bp.route('/roadtrip/<int:id>')
def roadtrip(id):
    roadtrip = read_roadtrip_internal(id)
    roadtrip_with_weather = populate_weather_data(roadtrip)
    guides = list_weather_guides(roadtrip_with_weather)
    temp_guide = list_temperature_guides(roadtrip_with_weather)
    points = [{'latitude': city['latitude'], 'longitude': city['longitude']}
              for city in roadtrip['cities']]
    return render_template('roadtrip.html', roadtrip=roadtrip_with_weather, points=points, guides=guides, temp_guide=temp_guide)


def populate_weather_data(roadtrip):
    roadtrip_with_weather = copy.deepcopy(roadtrip)
    for city in roadtrip_with_weather['cities']:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={city["latitude"]}&lon={city["longitude"]}&appid={current_app.config["SECRET_KEY"]}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        if weather_data['cod'] == 200:
            city['weather'] = {
                "id": weather_data['weather'][0]['id'],
                "description": weather_data['weather'][0]['description'],
                "temp": weather_data['main']['temp'],
                "icon": weather_data['weather'][0]['icon']
            }
    return roadtrip_with_weather


def list_weather_guides(roadtrip_with_weather):
    guides = []
    seen = set()
    for city in roadtrip_with_weather['cities']:
        weather_id = city['weather']['id']

        if weather_id not in seen:
            seen.add(weather_id)
            guide = WeatherGuide.query.get_or_404(weather_id)
            guides.append({
                "icon": city['weather']['icon'],
                "description": city['weather']['description'],
                "advice": guide.advice
            })

    return guides

def list_temperature_guides(roadtrip_with_weather):
    min_temp = float('inf')
    max_temp = float('-inf')

    for i in range(len(roadtrip_with_weather['cities'])):
        city = roadtrip_with_weather['cities'][i]
        temp = city['weather']['temp']
        min_temp = min(min_temp, temp)
        max_temp = max(max_temp, temp)

    amplitude = max_temp - min_temp

    min_advice = get_advice(min_temp)
    max_advice = get_advice(max_temp)

    amplitude_advice = ""
    if amplitude < 10:
        amplitude_advice = "Amplitude of temperature is very low, expect stable weather conditions."
    elif 10 <= amplitude < 20:
        amplitude_advice = "Amplitude of temperature is moderate, expect some variations in weather."
    else:
        amplitude_advice = "Amplitude of temperature is high, expect significant changes in weather conditions."

    return {
        "min_temp": round(min_temp),
        "max_temp": round(max_temp),
        "amplitude": amplitude,
        "min_advice": min_advice,
        "max_advice": max_advice,
        "amplitude_advice": amplitude_advice
    }
    
temperature_advices = {
    0: "Extreme caution required. Dangerously cold temperatures, dress in multiple layers and cover all exposed skin.",
    5: "Very cold. Wear a heavy winter jacket, hat, gloves, and scarf.",
    10: "Cold. Dress warmly with a coat, hat, and gloves.",
    15: "Cool. A light jacket or sweater may be sufficient.",
    20: "Mild. A light jacket or long sleeves might be comfortable.",
    25: "Warm. Dress in light layers.",
    30: "Very warm. Dress lightly and stay hydrated.",
    35: "Hot. Wear lightweight clothing and stay in the shade when possible.",
    40: "Very hot. Extreme caution required. Stay hydrated and seek air-conditioned spaces.",
}

def get_advice(temperature):
    """
    Get advice for travelers based on the temperature.
    """
    # Determine the appropriate advice based on the temperature
    for temp, advice in temperature_advices.items():
        if temperature <= temp:
            return advice