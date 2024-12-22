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
        # Handle structured Pydantic errors
        return jsonify({"error": "Validation failed", "details": str(e)}), 400        

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": "Internal Server Error"}), 500

