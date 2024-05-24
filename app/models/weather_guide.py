from app import db


class WeatherGuide(db.Model):
    __tablename__ = 'weather_guides'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    advice = db.Column(db.Text, nullable=False)
