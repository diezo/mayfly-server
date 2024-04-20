from flask import Blueprint
from .routes import create, end, delete

# Configurations
endpoint: str = "rooms"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(create.blueprint)
blueprint.register_blueprint(end.blueprint)
blueprint.register_blueprint(delete.blueprint)
