from flask import Blueprint
from .accounts import accounts
from .profile import profile
from .rooms import rooms

# Configurations
endpoint: str = "v1"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(accounts.blueprint, url_prefix="/accounts")
blueprint.register_blueprint(profile.blueprint, url_prefix="/profile")
blueprint.register_blueprint(rooms.blueprint, url_prefix="/rooms")
