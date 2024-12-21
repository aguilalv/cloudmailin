from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from cloudmailin.schemas import Email

bp = Blueprint("generic", __name__, url_prefix="/generic")


@bp.route("/new", methods=["POST"])
def new_generic_email():
    try:
        data_received = request.get_json()

        email = Email(**data_received)

        return (
            jsonify(
                {
                    "sender": email.sender,
                    "recipient": email.recipient,
                    "subject": email.subject,
                }
            ),
            200,
        )

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
