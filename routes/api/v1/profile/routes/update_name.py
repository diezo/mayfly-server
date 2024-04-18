from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from lib.Validator import Validator
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated

# Configurations
endpoint: str = "update-name"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
auth_collection: Collection = Database()["auth"]

# Libraries Initialization
session_manager: SessionManager = SessionManager(auth_collection)


@blueprint.patch(f"/{endpoint}")
@authenticated
def update_name(identifier: str) -> Response:
    """
    Endpoint to update profile information.
    :return: Response
    """

    try:
        # Gather Form Data
        full_name: str = request.json["full-name"]

        # Form Data Validation
        full_name_validated: tuple[bool, str] = Validator.full_name(full_name)

        if not full_name_validated[0]: return CommonExceptions.BadRequest(full_name_validated[1])

        # Update Data In Database
        auth_collection.update_one(
            filter={"_id": identifier},
            update={"$set": {"full_name": full_name}}
        )

        # Return Success
        return CommonSuccessions.DataUpdated("full_name", full_name)

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
