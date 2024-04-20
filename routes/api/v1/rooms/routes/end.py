from flask import Blueprint, Response, request
from structures.CreatedRoom import CreatedRoom
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.RoomManager import RoomManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated

# Configurations
endpoint: str = "end"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
rooms_collection: Collection = Database()["rooms"]
rooms_archive_collection: Collection = Database()["rooms-archive"]

# Libraries Initialization
room_manager: RoomManager = RoomManager(rooms_collection, rooms_archive_collection)


@blueprint.post(f"/{endpoint}/<room_id>")
@authenticated
def end(identifier: str, room_id: str) -> Response:
    """
    Endpoint to end room.
    :return: Response
    """

    # End Room
    end_response: tuple = room_manager.end_room(
        owner_id=identifier,
        room_id=room_id
    )

    # Parse Response
    ended: bool = end_response[0]
    response: Response = end_response[1]

    # Not Ended
    if not ended: return response

    # Return Success
    return CommonSuccessions.NoContentSuccess()
