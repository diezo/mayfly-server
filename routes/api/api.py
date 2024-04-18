from flask import Blueprint
from .v1 import v1

# Configurations
endpoint: str = "api"

# Create Blueprint
app: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
app.register_blueprint(v1.blueprint, url_prefix="/v1")
