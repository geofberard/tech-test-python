from app import app, db
from flask import Blueprint, request, jsonify
from app.models import Roadtrip, RoadtripCity

bp = Blueprint('api_roadtrips', __name__, url_prefix='/api/roadtrips')


@bp.route('/', methods=['GET'])
def get_all_roadtrips():
    """
    Retrieve all roadtrips.

    Returns:
        JSON response containing a list of all roadtrips with their ID and name.
    """
    roadtrips = Roadtrip.query.all()

    all_roadtrips = [{'id': roadtrip.id, 'name': roadtrip.name}
                     for roadtrip in roadtrips]

    return jsonify(all_roadtrips), 200


@bp.route('/', methods=['POST'])
def create_roadtrip():
    """
    Create a new roadtrip.

    Request JSON body:
        - name (str): The name of the roadtrip.

    Returns:
        JSON response with a success message.
    """
    data = request.get_json()
    name = data.get('name')

    newRoadtrip = Roadtrip(name=name)
    db.session.add(newRoadtrip)
    db.session.commit()

    return jsonify({"message": "RoadTrip added"}), 201


@bp.route('/<int:id>', methods=['GET'])
def read_roadtrip(id):
    """
    Retrieve a specific roadtrip by ID.

    Parameters:
        - id (int): The ID of the roadtrip.

    Returns:
        JSON response containing the roadtrip details and its associated cities.
    """
    return jsonify(read_roadtrip_internal(id))


@bp.route('/<int:id>', methods=['DELETE'])
def delete_roadtrip(id):
    """
    Delete a specific roadtrip by ID.

    Parameters:
        - id (int): The ID of the roadtrip.

    Returns:
        JSON response with a success message.
    """
    roadtrip = Roadtrip.query.get_or_404(id)

    db.session.delete(roadtrip)
    db.session.commit()

    return jsonify({"message": "RoadTrip deleted"}), 200


@bp.route('/<int:id>/add_city', methods=['POST'])
def add_city_to_roadtrip(id):
    """
    Add a city to a specific roadtrip by ID.

    Parameters:
        - id (int): The ID of the roadtrip.

    Request JSON body:
        - city_id (int): The ID of the city to be added.

    Returns:
        JSON response with a success message.
    """
    Roadtrip.query.get_or_404(id)

    max_position = db.session.query(db.func.max(
        RoadtripCity.position)).filter_by(roadtrip_id=id).scalar()

    if max_position is None:
        max_position = 0

    data = request.get_json()
    city_id = data.get('city_id')

    new_entry = RoadtripCity(
        roadtrip_id=id, city_id=city_id, position=max_position + 1)

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": f"City with ID {city_id} added to RoadTrip {id}"}), 200


@bp.route('/<int:id>/remove_city', methods=['DELETE'])
def remove_city_from_roadtrip(id):
    """
    Remove a city from a specific roadtrip by ID.

    Parameters:
        - id (int): The ID of the roadtrip.

    Request JSON body:
        - city_id (int): The ID of the city to be removed.

    Returns:
        JSON response with a success message.
    """
    Roadtrip.query.get_or_404(id)

    data = request.get_json()
    city_id = data.get('city_id')

    if city_id is None:
        return jsonify({"error": "City ID is required"}), 400

    link = RoadtripCity.query.filter(RoadtripCity.roadtrip_id == id).filter(
        RoadtripCity.city_id == city_id).first()

    db.session.delete(link)
    db.session.commit()

    return jsonify({"message": f"City with ID {city_id} removed from RoadTrip {id}"}), 200


def read_roadtrip_internal(id):
    """
    Internal function to retrieve a roadtrip by ID and its associated cities.

    Parameters:
        - id (int): The ID of the roadtrip.

    Returns:
        dict: A dictionary containing the roadtrip details and its associated cities.
    """
    roadtrip = Roadtrip.query.get_or_404(id)

    cities = (
        db.session.query(RoadtripCity)
        .filter_by(roadtrip_id=roadtrip.id)
        .order_by(RoadtripCity.position)
        .all()
    )

    city_list = [
        {
            "id": city.city.id, 
            "name": city.city.name,
            "country_code": city.city.country_code,
            "country_name": city.city.country_name,
            "admin_code": city.city.admin_code,
            "population": city.city.population,
            "elevation": city.city.elevation,
            "timezone": city.city.timezone,
            "latitude": city.city.latitude,
            "longitude": city.city.longitude
        } for city in cities
    ]

    return {
        "id": roadtrip.id,
        "name": roadtrip.name,
        "cities": city_list
    }
