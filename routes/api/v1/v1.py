from flask import Blueprint
from .accounts import accounts
from .profile import profile

# Configurations
endpoint: str = "v1"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(accounts.blueprint, url_prefix="/accounts")
blueprint.register_blueprint(profile.blueprint, url_prefix="/profile")
