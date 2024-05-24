from app import app
from flask import Blueprint, request, jsonify
from app.models import City

bp = Blueprint('api_cities', __name__, url_prefix='/api/cities')


@bp.route('/search', methods=['GET'])
def search_city():
    """
    Search for cities by name.

    Query Parameters:
        name (str): The name of the city to search for.

    Returns:
        A JSON response containing a list of cities that match the search criteria.
        Each city is represented as a dictionary with its details.
        If the name parameter is missing, returns a 400 error with a message.
    """
    city_name = request.args.get('name')
    if not city_name:
        return jsonify({"error": "Missing city name parameter"}), 400

    results = City.query.filter(City.name.ilike(f'%{city_name}%')).limit(10)
    cities = [
        {
            "id": city.id,
            "name": city.name,
            "country_code": city.country_code,
            "country_name": city.country_name,
            "admin_code": city.admin_code,
            "population": city.population,
            "elevation": city.elevation,
            "timezone": city.timezone,
            "latitude": city.latitude,
            "longitude": city.longitude
        } for city in results
    ]

    return jsonify(cities)
