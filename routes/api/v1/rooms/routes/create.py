from flask import Blueprint, Response, request
from structures.CreatedRoom import CreatedRoom
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from exceptions.SelfInvitedException import SelfInvitedException
from lib.RoomManager import RoomManager
from returns.commons import CommonExceptions, CommonSuccessions
from decorators.authentication import authenticated
from lib.RoomAuthenticator import RoomAuthenticator

# Configurations
endpoint: str = "create"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
rooms_collection: Collection = Database()["rooms"]

# Libraries Initialization
room_manager: RoomManager = RoomManager(rooms_collection)
room_authenticator: RoomAuthenticator = RoomAuthenticator()


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
        room_type: str = request.json.get("type", room_authenticator.ROOM_TYPES[0])
        access_type: str = request.json.get("access", room_authenticator.ACCESS_TYPES[0])
        passcode: str | None = request.json.get("passcode")
        invitees: list[str] | None = request.json.get("invitees")

        # Eliminate Extra Payload
        if room_type != room_authenticator.PASSCODE: passcode = None
        if room_type != room_authenticator.INVITE: invitees = None

        # Validate Passcode Settings
        if room_type == room_authenticator.PASSCODE and not room_authenticator.validate_passcode(passcode):
            return CommonExceptions.BadRequest("Please provide a room passcode.")

        # Validate Invitees Settings
        try:
            if room_type == room_authenticator.INVITE and not room_authenticator.validate_invitees(invitees, identifier):
                return CommonExceptions.BadRequest("Please provide a list of invitees.")

        # Self-Invited in Invitees List
        except SelfInvitedException:
            return CommonExceptions.BadRequest("You cannot include yourself in invitees.")

        # Verify Room-Type & Access-Type
        if room_type not in room_authenticator.ROOM_TYPES: room_type: str = room_authenticator.ROOM_TYPES[0]
        if access_type not in room_authenticator.ACCESS_TYPES: access_type: str = room_authenticator.ACCESS_TYPES[0]

        # Create Room
        room: CreatedRoom = room_manager.create_room(
            owner_id=identifier,
            room_type=room_type,
            access_type=access_type,
            room_title=room_title,
            room_description=room_description,
            passcode=passcode,
            invitees=invitees
        )

        # Return Success
        return CommonSuccessions.RoomCreated(room.room_id)

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
