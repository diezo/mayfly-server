import json
from flask import Blueprint, Response, request
from werkzeug.exceptions import UnsupportedMediaType
from pymongo.errors import OperationFailure
from lib.Database import Database
from pymongo.collection import Collection
from hashlib import sha512
from random import choices

app: Blueprint = Blueprint("ajax", __name__)
auth_collection: Collection = Database()["auth"]

SESSION_ID_LENGTH: int = 80
SESSION_ID_ALLOWED_CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MAX_SESSIONS_COUNT: int = 7


# Login Endpoint
@app.get("/ajax")
def ajax():
    try:
        email: str = request.json["email"]
        password: str = request.json["password"]

        auth_user: dict = auth_collection.find_one({"email": email})
        identifier: str = auth_user["_id"]

        # Email not registered
        if auth_user is None:
            return Response(
                json.dumps({"status": "fail", "error": "Email isn't registered."}),
                401
            )

        # Calculate password hashes
        password_sha512_hash: str = auth_user.get("password_sha512_hash")
        password_sha512_hash_provided: str = sha512(password.encode("utf-8")).hexdigest()

        # Database don't have required password hash
        if password_sha512_hash is None:
            if auth_user is None:
                return Response(
                    json.dumps({"status": "fail", "error": "Sorry, something's wrong on our side."}),
                    500
                )

        # Passwords match
        if password_sha512_hash == password_sha512_hash_provided:
            return Response(
                json.dumps({"status": "ok", "identifier": identifier, "session_id": new_session(identifier)}),
                200
            )

        # Passwords don't match
        return Response(
            json.dumps({"status": "fail", "error": "Incorrect password."}),
            401
        )

    #
    except KeyError:
        return Response(
            json.dumps({"status": "fail", "error": "Required keys not in body json."}),
            400,
            content_type="text/json"
        )

    except UnsupportedMediaType:
        return Response(
            json.dumps({"status": "fail", "error": "Cannot parse body json."}),
            400,
            content_type="text/json"
        )


def new_session(identifier: str):
    """
    Generates a new session_id for the current user.
    :return: Response
    """

    # Create new session_id
    session_id: str = str().join(choices(SESSION_ID_ALLOWED_CHARS, k=SESSION_ID_LENGTH))

    # Get sessions count
    try:
        sessions_count: int = list(auth_collection.aggregate(
            pipeline=[
                {"$match": {"_id": identifier}},
                {"$project": {"sessions_count": {"$size": "$sessions"}}}
            ]
        ))[0]["sessions_count"]

    except OperationFailure: sessions_count: int = 0

    # Slice sessions to comply with MAX_SESSIONS_COUNT
    if sessions_count >= MAX_SESSIONS_COUNT:

        # Fetch sessions list
        existing_sessions: list[list[str]] = auth_collection.find_one(
            {"_id": identifier},
            {"_id": 0, "sessions": 1}
        )["sessions"]

        # Sliced sessions list
        sliced_sessions: list[list[str]] = existing_sessions[len(existing_sessions) - MAX_SESSIONS_COUNT + 1:]

        # Append new session to sliced list
        sliced_sessions.append([session_id])

        # Update sessions with sliced list
        auth_collection.update_one(
            filter={"_id": identifier},
            update={"$set": {"sessions": sliced_sessions}}
        )

    else:
        # Register new session
        auth_collection.update_one(
            filter={"_id": identifier},
            update={"$push": {"sessions": [session_id]}}
        )

    return session_id
