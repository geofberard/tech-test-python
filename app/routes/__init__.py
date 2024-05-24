from .site import bp as site_bp
from .api_cities import bp as api_cities_bp
from .api_roadtrips import bp as api_roadtrips_bp


def register_blueprints(app):
    app.register_blueprint(site_bp)
    app.register_blueprint(api_cities_bp)
    app.register_blueprint(api_roadtrips_bp)
