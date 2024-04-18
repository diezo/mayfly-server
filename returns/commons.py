from typing import Callable
from flask import Response
import json


class CommonExceptions:

    BadRequest: Callable[[str], Response] = staticmethod(lambda error: Response(
        response=json.dumps({"status": "fail", "error": error}),
        status=400,
        content_type="text/json"
    ))

    NotFound: Callable[[str], Response] = staticmethod(lambda error: Response(
        response=json.dumps({"status": "fail", "error": error}),
        status=404,
        content_type="text/json"
    ))

    Forbidden: Callable[[str], Response] = staticmethod(lambda error: Response(
        response=json.dumps({"status": "fail", "error": error}),
        status=403,
        content_type="text/json"
    ))


class CommonSuccessions:

    Success: Callable[[str], Response] = staticmethod(lambda message: Response(
        response=json.dumps({"status": "ok", "message": message}),
        status=200,
        content_type="text/json"
    ))

    OTPSent: Callable[[str], Response] = staticmethod(lambda registration_token: Response(
        response=json.dumps({"status": "ok", "otp_sent": True, "registration_token": registration_token}),
        status=200,
        content_type="text/json"
    ))

    AccountCreated: Callable[[], Response] = staticmethod(lambda: Response(
        response=json.dumps({"status": "ok", "account_created": True}),
        status=200,
        content_type="text/json"
    ))
