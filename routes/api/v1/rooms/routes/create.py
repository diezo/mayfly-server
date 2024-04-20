from flask import Blueprint, Response, request
from structures.CreatedRoom import CreatedRoom
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.RoomManager import RoomManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated

# Configurations
endpoint: str = "create"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
rooms_collection: Collection = Database()["rooms"]

# Libraries Initialization
room_manager: RoomManager = RoomManager(rooms_collection)


@blueprint.post(f"/{endpoint}")
@authenticated
def create(identifier: str) -> Response:
    """
    Endpoint to create room.
    :return: Response
    """

    try:
        # Gather Information
        room_title: str = request.json.get("title")
        room_description: str = request.json.get("description")

        # Create Room
        room: CreatedRoom = room_manager.create_room(
            owner_id=identifier,
            room_title=room_title,
            room_description=room_description
        )

        # Return Success
        return CommonSuccessions.RoomCreated(room.room_id)

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
