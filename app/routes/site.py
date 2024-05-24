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
    points = [{'latitude': city['latitude'], 'longitude': city['longitude']}
              for city in roadtrip['cities']]
    return render_template('roadtrip.html', roadtrip=roadtrip_with_weather, points=points, guides=guides)


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
