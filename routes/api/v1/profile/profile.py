from flask import Blueprint
from .routes import register

# Configurations
endpoint: str = "profile"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(register.blueprint)
