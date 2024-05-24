from app import db


class RoadtripCity(db.Model):
    """
    RoadtripCity model representing the relationship between roadtrips and cities.

    Attributes:
        id (int): Primary key for the roadtrip city relationship.
        roadtrip_id (int): Foreign key referencing the roadtrip.
        city_id (int): Foreign key referencing the city.
        position (int): Position of the city in the roadtrip.
    """
    __tablename__ = 'roadtrip_cities'
    
    id = db.Column(db.Integer, primary_key=True)
    roadtrip_id = db.Column(db.Integer, db.ForeignKey(
        'roadtrips.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)

    roadtrip = db.relationship('Roadtrip', back_populates='cities')
    city = db.relationship('City', back_populates='roadtrips')

    def __repr__(self):
        """
        Provides a string representation of a RoadtripCity instance.

        Returns:
            str: A string representation of the RoadtripCity instance.
        """
        return f'<RoadtripCity {self.roadtrip_id} - {self.city_id} (Position: {self.position})>'
