from flask import Blueprint, Response

app: Blueprint = Blueprint("ajax", __name__)


# Login Endpoint
@app.get("/ajax")
def ajax():
    return Response("Login endpoint", 200)
