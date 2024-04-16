from flask import Blueprint
from .v1 import v1

app: Blueprint = Blueprint("api", __name__)

# Register Blueprints
app.register_blueprint(v1.app, url_prefix="/v1")
