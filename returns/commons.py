from typing import Callable
from flask import Response
import json


class CommonExceptions:

    BadRequest: Callable[[str], Response] = staticmethod(lambda error: Response(
        response=json.dumps({"static": "fail", "error": error}),
        status=400,
        content_type="text/json"
    ))


class CommonSuccessions:

    Success: Callable[[str], Response] = staticmethod(lambda message: Response(
        response=json.dumps({"status": "ok", "message": message}),
        status=200,
        content_type="text/json"
    ))
