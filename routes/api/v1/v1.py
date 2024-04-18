from flask import Blueprint
from .accounts import accounts

# Configurations
endpoint: str = "v1"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(accounts.blueprint, url_prefix="/accounts")
