from dataclasses import dataclass


@dataclass
class CreatedRoom:
    """
    Contains information about the room just created.
    """

    room_id: str
