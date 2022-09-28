import logging
import os

from flask import Flask, jsonify, request
from flask_expects_json import expects_json

from db import db_api
from app.services.users.alerter import Alerter as UserAlerter


flask_app = Flask(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
flask_app.logger.handlers = gunicorn_logger.handlers
flask_app.logger.setLevel(gunicorn_logger.level)

WHITE_LISTED_PARAMS = ["amount", "t", "type", "user_id"]

schema = {
    "type": "object",
    "properties": {
        "amount": {"type": "string"},
        "t": {"type": "string"},
        "type": {"type": "string"},
        "user_id": {"type": "string"},
    },
    "required": ["amount" "t" "type" "user_id"],
}


@flask_app.route("/v1/event/", methods=["POST"])
@expects_json(schema)
def v1_event():
    request_data = request.get_json()
    user_id = request_data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    db_api.EventDAO().create(**_filtered_request_data(request_data))

    alert_codes = _alert_codes(user_id)

    return jsonify(
        {
            "alert": any(alert_codes),
            "alert_codes": alert_codes,
            "user_id": user_id,
        }
    )


# private


def _alert_codes(user_id) -> list:
    return UserAlerter(user_id).alert_codes()


def _filtered_request_data(request_data_raw: dict) -> dict:
    white_listed_request_data = _white_listed_request_data(request_data_raw)

    return {
        ("client_timestamp" if k == "t" else k): v
        for (k, v) in white_listed_request_data.items()
    }


def _white_listed_request_data(request_data_raw) -> dict:
    return {
        key: request_data_raw.get(key)
        for key in WHITE_LISTED_PARAMS
        if request_data_raw.get(key)
    }
