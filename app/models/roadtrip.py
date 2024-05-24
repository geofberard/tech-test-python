from app import db


class Roadtrip(db.Model):
    """
    Roadtrip model representing a roadtrip in the database.

    Attributes:
        id (int): Primary key for the roadtrip.
        name (str): Name of the roadtrip.
        cities (list[RoadtripCity]): List of cities associated with the roadtrip.
    """
    __tablename__ = 'roadtrips'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    cities = db.relationship(
        'RoadtripCity', back_populates='roadtrip', cascade='all, delete-orphan'
    )

    def __repr__(self):
        """
        Provides a string representation of a Roadtrip instance.

        Returns:
            str: A string representation of the Roadtrip instance.
        """
        return f'<Roadtrip {self.name}>'
