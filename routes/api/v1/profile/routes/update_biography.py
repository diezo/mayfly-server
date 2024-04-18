from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from lib.Validator import Validator
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated

# Configurations
endpoint: str = "update-biography"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
auth_collection: Collection = Database()["auth"]

# Libraries Initialization
session_manager: SessionManager = SessionManager(auth_collection)


@blueprint.patch(f"/{endpoint}")
@authenticated
def update_biography(identifier: str) -> Response:
    """
    Endpoint to update profile information.
    :return: Response
    """

    try:
        # Gather Form Data
        biography: str = request.json["biography"]

        # Form Data Validation
        biography_validated: tuple[bool, str] = Validator.biography(biography)

        if not biography_validated[0]: return CommonExceptions.BadRequest(biography_validated[1])

        # Update Data In Database
        auth_collection.update_one(
            filter={"_id": identifier},
            update={"$set": {"biography": biography}}
        )

        # Return Success
        return CommonSuccessions.DataUpdated("biography", biography)

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
