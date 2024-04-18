import json
from flask import Blueprint, Response, request
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.Database import Database
from lib.Validator import Validator
from pymongo.collection import Collection
from hashlib import sha512
from returns.commons import CommonExceptions
from lib.SessionManager import SessionManager

# Configurations
endpoint: str = "login"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
auth_collection: Collection = Database()["auth"]
session_manager: SessionManager = SessionManager(auth_collection)


@blueprint.post(f"/{endpoint}")
def login() -> Response:
    """
    Endpoint to log into an existing account.
    :return: Response
    """
    try:
        # Gather Form Data
        email: str = request.json["email"]
        password: str = request.json["password"]

        # Form Data Validation
        email_validated: tuple[bool, str] = Validator.email(email)
        password_validated: tuple[bool, str] = Validator.password(password)

        if not email_validated[0]: return CommonExceptions.BadRequest(email_validated[1])
        if not password_validated[0]: return CommonExceptions.BadRequest(password_validated[1])

        # Fetching Auth User From Database
        auth_user: dict = auth_collection.find_one({"email": email})

        # No Such Account
        if auth_user is None:
            return Response(
                json.dumps({"status": "fail", "error": "Email isn't registered."}),
                401
            )

        # Get Identifier
        identifier: str = auth_user["_id"]

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
            return Response(json.dumps(
                {
                    "status": "ok",
                    "identifier": identifier,
                    "session_id": session_manager.new_session(identifier)
                }),
                status=200
            )

        # Passwords don't match
        return Response(
            json.dumps({"status": "fail", "error": "Incorrect password."}),
            status=401
        )

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
