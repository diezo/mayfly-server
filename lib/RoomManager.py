from pymongo.collection import Collection
from flask import Response
from structures.CreatedRoom import CreatedRoom
from returns.commons import CommonExceptions
from random import choices
import datetime


class RoomManager:

    # Database Collections
    rooms_collection: Collection
    rooms_archive_collection: Collection

    # Configuration
    ROOM_ID_ALLOWED_CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ROOM_ID_LENGTH: int = 20

    def __init__(self, rooms_collection: Collection, rooms_archive_collection: Collection = None) -> None:
        """
        Initializes this class.
        :param rooms_collection: MongoDB Collection Object
        :param rooms_archive_collection: MongoDB Collection Object
        """

        self.rooms_collection = rooms_collection
        self.rooms_archive_collection = rooms_archive_collection

    def create_room(
            self,
            owner_id: str,
            room_title: str = None,
            room_description: str = None
    ) -> CreatedRoom:
        """
        Registers a new room in database.
        :param owner_id: Owner Identifier
        :param room_title: Room Title
        :param room_description: Room's Short Description
        :return: CreatedRoom Object with Room's Information
        """

        # Room Details
        room_id: str = self.new_room_id()

        # Prepare Database Entry
        entry: dict = {
            "_id": room_id,
            "owner_id": owner_id,
            "created-timestamp": self.timestamp_now()
        }

        # Append Optional Data To Entry
        if room_title is not None: entry["title"] = room_title
        if room_description is not None: entry["description"] = room_description

        # Add Room in Database
        self.rooms_collection.insert_one(entry)

        # Return Information
        return CreatedRoom(room_id=room_id)

    def end_room(
            self,
            owner_id: str,
            room_id: str = None
    ) -> tuple[bool, Response | None]:
        """
        Deletes the room from database and moves it to archive.
        :param owner_id: Owner Identifier
        :param room_id: Room's ID
        :return: Ended (Boolean), Response (On Exception)
        """

        # Room Details
        room: dict = self.rooms_collection.find_one({"_id": room_id})

        # Doesn't Exist
        if room is None: return False, CommonExceptions.Forbidden("No such room was found.")

        # Room Ownership Verification
        if room.get("owner_id", "") != owner_id:
            return False, CommonExceptions.RoomOwnershipError()

        # Move To Archive
        self.rooms_archive_collection.insert_one(room)

        # Delete Room
        self.rooms_collection.delete_one({"_id": room_id})

        # Return State
        return True, None

    def delete_room(
            self,
            owner_id: str,
            room_id: str = None
    ) -> tuple[bool, Response | None]:
        """
        Deletes the room from archive.
        :param owner_id: Owner Identifier
        :param room_id: Room's ID
        :return: Deleted (Boolean), Response (On Exception)
        """

        # Make Sure Room Is Not Active
        if self.rooms_collection.find_one({"_id": room_id}) is not None:
            return False, CommonExceptions.Forbidden("Rooms isn't ended yet.")

        # Fetch Archive Room Details
        archived_room: dict = self.rooms_archive_collection.find_one({"_id": room_id})

        # Doesn't Exist
        if archived_room is None: return False, CommonExceptions.Forbidden("No such room was found in archive.")

        # Room Ownership Verification
        if archived_room.get("owner_id", "") != owner_id:
            return False, CommonExceptions.RoomOwnershipError()

        # Delete From Archive
        self.rooms_archive_collection.delete_one({"_id": room_id})

        # Return State
        return True, None

    @staticmethod
    def timestamp_now() -> int:
        """
        Generates the current timestamp.
        :return: Timestamp (String)
        """

        return int(datetime.datetime.now().timestamp())

    def new_room_id(self) -> str:
        """
        Generates a new room id.
        :return: Room ID (String)
        """

        return str().join(choices(self.ROOM_ID_ALLOWED_CHARS, k=self.ROOM_ID_LENGTH))
