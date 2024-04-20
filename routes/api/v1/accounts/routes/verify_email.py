from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions
from lib.mails.WelcomeEmail import WelcomeEmail
from hashlib import sha512
from bson import ObjectId

# Configurations
endpoint: str = "verify-email"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
auth_collection: Collection = Database()["auth"]
hold_accounts_collection: Collection = Database()["held-accounts"]

# Libraries Initialization
session_manager: SessionManager = SessionManager(auth_collection)
welcome_email: WelcomeEmail = WelcomeEmail()


@blueprint.post(f"/{endpoint}")
def verify_email() -> Response:
    """
    Endpoint to verify email of accounts on-hold.
    :return: Response
    """

    try:
        # Gather Form Data
        email: str = request.json["email"]
        password: str = request.json["password"]
        registration_token: str = request.json["registration_token"]
        otp: str = request.json["otp"]
        password_hash: str = sha512(password.encode("utf-8")).hexdigest()

        # Fetch On-Hold Account
        held_account: dict = hold_accounts_collection.find_one(
            filter={"email": email, "password_sha512_hash": password_hash, "registration_token": registration_token},
            projection={"_id": 0, "otp": 1}
        )

        # Held-Account Not Found
        if held_account is None: return CommonExceptions.NotFound("Sorry, something went wrong.")

        # Compare OTPs - Incorrect
        if otp != held_account.get("otp", ""): return CommonExceptions.Forbidden("Incorrect OTP.")

        # Register Account In Database
        auth_collection.insert_one({
            "_id": str(ObjectId()),
            "email": email,
            "password_sha512_hash": password_hash
        })

        # Delete Held-Account(s) From Database
        hold_accounts_collection.delete_many({"email": email})

        # Send Welcome Email!
        welcome_email.send(email)

        # Return Success Message
        return CommonSuccessions.AccountCreated()

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
