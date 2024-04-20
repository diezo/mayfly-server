from string import digits
from exceptions.SelfInvitedException import SelfInvitedException


class RoomAuthenticator:
    """
    Manages room authentication.
    """

    # Configurations
    PASSCODE_LENGTHS: int = [4, 6]
    MINIMUM_INVITEES_COUNT: int = 1

    # Authentication Types
    ROOM_TYPES: list[str] = ["public", "passcode", "invite"]
    ACCESS_TYPES: list[str] = ["open", "approval"]

    # Short Titles
    PUBLIC: str = "public"
    PASSCODE: str = "passcode"
    INVITE: str = "invite"
    OPEN: str = "open"
    APPROVAL: str = "approval"

    # Defaults
    DEFAULT_ROOM_TYPE: str = ROOM_TYPES[0]
    DEFAULT_ACCESS_TYPE: str = ACCESS_TYPES[0]

    def validate_passcode(self, passcode: str) -> bool:
        """
        Validates if a passcode is appropriate.
        :param passcode: Passcode (String)
        :return: Appropriate (Boolean)
        """

        if passcode is None: return False  # None
        if type(passcode) is not str: return False  # Not String
        if True in [True for x in passcode if x not in digits]: return False  # Includes Restricted Characters
        if len(passcode) not in self.PASSCODE_LENGTHS: return False  # Inappropriate Length

        return True  # Looks Good!

    def validate_invitees(self, invitees: list[str], identifier: str) -> bool:
        """
        Validates if a list of invitees is appropriate.
        :param invitees: List of Invitees' Usernames (List of Strings)
        :param identifier: User's Identifier
        :return: Appropriate (Boolean)
        """

        if invitees is None: return False  # None
        if type(invitees) is not list: return False  # Not List
        if True in [True for x in invitees if type(x) is not str]: return False  # All Members Not String
        if identifier in invitees: raise SelfInvitedException()  # Can't Include Self
        if True in [True for x in invitees if len(x) <= 0]: return False  # One-or-more Empty Strings
        if len(invitees) < self.MINIMUM_INVITEES_COUNT: return False  # Inappropriate List Length

        return True  # Looks Good!
