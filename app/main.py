import logging
import os
from uuid import UUID

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


flask_app = Flask(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
flask_app.logger.handlers = gunicorn_logger.handlers
flask_app.logger.setLevel(gunicorn_logger.level)
db = SQLAlchemy(flask_app)


@flask_app.route("/v1/event/", methods=["POST"])
def v1_event():
    request_data = request.get_json()

    if not request_data.get("user_id"):
        return jsonify({"error": "user_id is required"}), 400

    return jsonify(
        {
            "alert": _alert(request_data),
            "alert_codes": _alert_codes(request_data),
            "user_id": _user_id(request_data),
        }
    )


# private


def _alert(request_data: dict) -> bool:
    return any(_alert_codes(request_data))


def _alert_codes(request_data: dict) -> list:
    # eg: [30, 123]
    # Delegate to UserAlerter class
    return []


def _user_id(request_data: dict) -> UUID:
    return request_data["user_id"]
