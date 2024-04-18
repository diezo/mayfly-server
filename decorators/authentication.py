from flask import request
from typing import Callable
from returns.commons import CommonExceptions
from pymongo.collection import Collection
from lib.Database import Database

# Database Collections
auth_collection: Collection = Database()["auth"]


def authenticated(method: Callable) -> Callable:
    """
    Allows execution of method only if user is authenticated.

    :param method: Authenticated Method
    :return: Callable
    """

    def wrapper():
        """
        Analyzes main function and executes it if user is authenticated.
        :return:
        """

        # Parse Bearer Token
        try: bearer: list[str] = [x.strip() for x in str(request.authorization).strip().split(" ")[1].strip().split(":")]
        except IndexError: return CommonExceptions.Unauthenticated()

        # Contains Identifier & SessionID?
        if len(bearer) != 2: return CommonExceptions.Unauthenticated()

        # Validate Through Database
        account: dict = auth_collection.find_one(
            filter={"_id": bearer[0], "sessions": [bearer[1]]},
            projection={"_id": 1}
        )

        # Final Decision
        if account is not None: return method(bearer[0])  # Authorized
        else: return CommonExceptions.Unauthenticated()  # Unauthorized

    return wrapper
