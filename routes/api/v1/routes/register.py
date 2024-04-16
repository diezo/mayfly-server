from flask import Blueprint, Response

app: Blueprint = Blueprint("register", __name__)


# Registration Endpoint
@app.get("/register")
def register():
    return Response("Registration Endpoint", 200)
