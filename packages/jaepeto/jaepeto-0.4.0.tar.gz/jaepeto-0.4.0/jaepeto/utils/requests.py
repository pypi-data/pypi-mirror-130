"""
Making requests to server
"""
import hashlib
import json
import os
from typing import List, Union

import requests

SERVER_DOMAIN = "https://x0jfh97rfl.execute-api.eu-west-2.amazonaws.com/Prod/"


def post(endpoint: str, payload: Union[str, List[str]]) -> Union[None, str, List[str]]:
    hashed_project = hashlib.sha224(
        os.environ["JAEPETO_PROJECT_NAME"].encode("utf-8")
    ).hexdigest()

    _run_locally = (
        "JAEPETO_RUN_LOCALLY" in os.environ
        and os.environ["JAEPETO_RUN_LOCALLY"] == "True"
    )
    _server_domain = SERVER_DOMAIN if not _run_locally else "http://127.0.0.1:3000/"

    try:
        response = requests.post(
            _server_domain + endpoint + f"?project={hashed_project}",
            data=json.dumps(payload),
            headers={
                "x-api-key": os.environ["JAEPETO_API_KEY"],
                "content-type": "application/json",
            },
        )
    except requests.exceptions.ConnectionError:
        # Happens if running locally but server hasn't set up (or API server has crashed!)
        return None

    if response.status_code == 200:
        message = response.json()["message"]
        if isinstance(message, list):
            return message

        try:
            message = json.loads(message)
        except Exception:
            pass
        return message
    else:
        return None
