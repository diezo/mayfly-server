from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.Validator import Validator
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions
from hashlib import sha512
from lib.mails.OTPEmailVerification import OTPEmailVerification

# Configurations
endpoint: str = "register"

# Create Blueprint
blueprint: Blueprint = Blueprint(endpoint, __name__)

# Database Collections
hold_accounts_collection: Collection = Database()["held-accounts"]
auth_collection: Collection = Database()["auth"]

# Libraries Initialization
session_manager: SessionManager = SessionManager(auth_collection)
otp_email_verification: OTPEmailVerification = OTPEmailVerification()


@blueprint.post(f"/{endpoint}")
def register() -> Response:
    """
    Endpoint to register a new account.
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

        # Check If Email Already Registered
        if auth_collection.find_one({"email": email}) is not None: return CommonExceptions.Forbidden(
            "Email already registered."
        )

        # Generate Tokens
        registration_token: str = session_manager.new_registration_token()
        otp: str = session_manager.new_otp()

        # Delete Previous Accounts (On Hold)
        hold_accounts_collection.delete_many({"email": email})

        # Register Account In Database (On Hold)
        hold_accounts_collection.insert_one({
            "email": email,
            "password_sha512_hash": sha512(password.encode("utf-8")).hexdigest(),
            "registration_token": registration_token,
            "otp": otp
        })

        # Send Verification Email
        otp_email_verification.send(email, otp)

        # Return Success Message
        return CommonSuccessions.OTPSent(registration_token)

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
