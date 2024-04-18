from pymongo.collection import Collection
from random import choices
from pymongo.errors import OperationFailure


class SessionManager:

    # Database Collections
    auth_collection: Collection

    # About Session IDs (For Logged-In Accounts)
    SESSION_ID_LENGTH: int = 80
    SESSION_ID_ALLOWED_CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    MAX_SESSIONS_COUNT: int = 7

    # About Registration Tokens (For Accounts Being On-Hold)
    REGISTRATION_TOKEN_ALLOWED_CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    REGISTRATION_TOKEN_LENGTH: int = 600

    # About OTPs (For Email Verification)
    OTP_ALLOWED_CHARS: str = "0123456789"
    OTP_LENGTH: int = 6

    def __init__(self, auth_collection: Collection) -> None:
        """
        Initializes SessionManager Class.
        :param auth_collection: Instance of MongoDB's Collection Class
        """

        self.auth_collection = auth_collection

    def new_session(self, identifier: str):
        """
        Generates a new session_id for the current user.
        :return: Response
        """

        # Create new session_id
        session_id: str = str().join(choices(self.SESSION_ID_ALLOWED_CHARS, k=self.SESSION_ID_LENGTH))

        # Get sessions count
        try:
            sessions_count: int = list(self.auth_collection.aggregate(
                pipeline=[
                    {"$match": {"_id": identifier}},
                    {"$project": {"sessions_count": {"$size": "$sessions"}}}
                ]
            ))[0]["sessions_count"]

        # No Sessions Yet
        except (OperationFailure, IndexError):
            sessions_count: int = 0

        # Slice sessions to comply with MAX_SESSIONS_COUNT
        if sessions_count >= self.MAX_SESSIONS_COUNT:

            # Fetch sessions list
            existing_sessions: list[list[str]] = self.auth_collection.find_one(
                {"_id": identifier},
                {"_id": 0, "sessions": 1}
            )["sessions"]

            # Sliced sessions list
            sliced_sessions: list[list[str]] = existing_sessions[len(existing_sessions) - self.MAX_SESSIONS_COUNT + 1:]

            # Append new session to sliced list
            sliced_sessions.append([session_id])

            # Update sessions with sliced list
            self.auth_collection.update_one(
                filter={"_id": identifier},
                update={"$set": {"sessions": sliced_sessions}}
            )

        else:
            # Register new session
            self.auth_collection.update_one(
                filter={"_id": identifier},
                update={"$push": {"sessions": [session_id]}}
            )

        return session_id

    def new_registration_token(self) -> str:
        """
        Generates a new registration token for accounts to be kept on hold.
        :return: registration_token (String)
        """

        return str().join(choices(self.REGISTRATION_TOKEN_ALLOWED_CHARS, k=self.REGISTRATION_TOKEN_LENGTH))

    def new_otp(self) -> str:
        """
        Generates a new OTP for accounts to verify their email.
        :return: otp (String)
        """

        return str().join(choices(self.OTP_ALLOWED_CHARS, k=self.OTP_LENGTH))
