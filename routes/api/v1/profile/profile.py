from flask import Blueprint
from .routes import update_name, update_biography

# Configurations
endpoint: str = "profile"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(update_name.blueprint)
blueprint.register_blueprint(update_biography.blueprint)
