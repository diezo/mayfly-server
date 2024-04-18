from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions

# Configurations
endpoint: str = "update"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
auth_collection: Collection = Database()["auth"]

session_manager: SessionManager = SessionManager(auth_collection)


@blueprint.patch(f"/{endpoint}")
def update() -> Response:
    """
    Endpoint to update profile information.
    :return: Response
    """

    try:
        # Authenticate
        ...

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
