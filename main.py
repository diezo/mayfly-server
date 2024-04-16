from flask import Flask
from routes.api import api

production: bool = False
app: Flask = Flask(__name__)

# Register Blueprints
app.register_blueprint(api.app, url_prefix="/api")

# Run server
app.run(port=80, debug=not production)
