from flask import Blueprint
from .routes import login, register, verify_email

# Configurations
endpoint: str = "accounts"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Register Blueprints
blueprint.register_blueprint(login.blueprint)
blueprint.register_blueprint(register.blueprint)
blueprint.register_blueprint(verify_email.blueprint)
