from flask import Blueprint
from .routes import ajax, register

app: Blueprint = Blueprint("v1", __name__)

# Register Blueprints
app.register_blueprint(ajax.app)
app.register_blueprint(register.app)
