from flask import Blueprint, Response, request
from pymongo.collection import Collection
from lib.Database import Database
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from lib.Validator import Validator
from lib.SessionManager import SessionManager
from returns.commons import CommonExceptions, CommonSuccessions
from hashlib import sha512
from lib.mails.EmailVerification import EmailVerification

blueprint: Blueprint = Blueprint("register", __name__)

# Database Collections
hold_accounts_collection: Collection = Database()["hold-accounts"]
auth_collection: Collection = Database()["auth"]

session_manager: SessionManager = SessionManager(auth_collection)
email_verification: EmailVerification = EmailVerification()


@blueprint.post("/register")
def register() -> Response:
    """
    Endpoint to register a new account.
    :return: Response
    """

    try:
        # Gather Form Data
        email: str = request.json["email"]
        password: str = request.json["password"]
        full_name: str = request.json["full_name"]

        # Form Data Validation
        email_validated: tuple[bool, str] = Validator.email(email)
        password_validated: tuple[bool, str] = Validator.password(password)
        full_name_validated: tuple[bool, str] = Validator.full_name(full_name)

        if not email_validated[0]: return CommonExceptions.BadRequest(email_validated[1])
        if not password_validated[0]: return CommonExceptions.BadRequest(password_validated[1])
        if not full_name_validated[0]: return CommonExceptions.BadRequest(full_name_validated[1])

        registration_token: str = session_manager.new_registration_token()

        # Delete Previous Accounts (On Hold)
        hold_accounts_collection.delete_many({"email": email})

        # Register Account In Database (On Hold)
        hold_accounts_collection.insert_one({
            "email": email,
            "password_sha512_hash": sha512(password.encode("utf-8")).hexdigest(),
            "registration_token": registration_token
        })

        # Send Verification Email
        email_verification.send(full_name, email, registration_token)

        # Return Success Message
        return CommonSuccessions.Success(
            "We've sent you an email with a verification link to proceed further. "
            "Please check your inbox as well as junk folder."
        )

    # Not Enough Form Data
    except KeyError:
        return CommonExceptions.BadRequest("Required keys not in body json.")

    # Invalid Form Data
    except (UnsupportedMediaType, BadRequest):
        return CommonExceptions.BadRequest("Cannot parse body json.")
