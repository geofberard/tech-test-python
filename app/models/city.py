from app import db


class City(db.Model):
    """
    City model representing a city in the database.

    Attributes:
        id (int): Primary key for the city.
        name (str): Name of the city.
        country_code (str): ISO country code of the city.
        country_name (str): Name of the country the city is located in.
        admin_code (str): Administrative code for the city.
        population (int): Population of the city.
        elevation (int): Elevation of the city in meters.
        timezone (str): Timezone of the city.
        latitude (float): Latitude coordinate of the city.
        longitude (float): Longitude coordinate of the city.
    """
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    country_code = db.Column(db.String(512))
    country_name = db.Column(db.String(512))
    admin_code = db.Column(db.String(512))
    population = db.Column(db.Integer)
    elevation = db.Column(db.Integer)
    timezone = db.Column(db.String(512))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    roadtrips = db.relationship(
        'RoadtripCity', back_populates='city', cascade='all, delete-orphan'
    )

    def __repr__(self):
        """
        Provides a string representation of a City instance.

        Returns:
            str: A string representation of the City instance.
        """
        return f'<City {self.name}, {self.country_name}>'
