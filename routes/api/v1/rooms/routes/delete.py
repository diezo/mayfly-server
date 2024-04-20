from flask import Blueprint, Response, request
from structures.CreatedRoom import CreatedRoom
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.RoomManager import RoomManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated

# Configurations
endpoint: str = "delete"

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
    Endpoint to delete room from archive.
    :return: Response
    """

    # Delete Room
    delete_response: tuple = room_manager.delete_room(
        owner_id=identifier,
        room_id=room_id
    )

    # Parse Response
    deleted: bool = delete_response[0]
    response: Response = delete_response[1]

    # Not Deleted
    if not deleted: return response

    # Return Success
    return CommonSuccessions.NoContentSuccess()
