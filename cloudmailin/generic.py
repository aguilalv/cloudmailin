from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from cloudmailin.schemas import Email

from icecream import ic

bp = Blueprint("generic", __name__, url_prefix="/generic")


@bp.route("/new", methods=["POST"])
def new_generic_email():
    try:
        data_received = request.get_json()
        email = Email(**data_received)

        # Step 1: Retrieve the handler registry from the app context
        handler_registry = current_app.config.get("handler_registry")
        if not handler_registry:
            raise RuntimeError("Handler registry is not configured in the app context.")

        # Step 2: Retrieve the appropriate handler
        handler_class = handler_registry.get_handler_for_sender(email.sender)
        handler = handler_class()

        # Step 3: Process the email using the handler
        handler.handle(email)

        return (
            jsonify(
                {
                    "sender": email.sender,
                    "recipient": email.recipient,
                    "subject": email.subject,
                    "date": email.date,
                    "plain": email.plain,
                    "html": email.html,
                }
            ),
            200,
        )

    except ValidationError as e:
        # Handle structured Pydantic errors
        return jsonify({"error": "Validation failed", "details": str(e)}), 400

    except Exception as e:
        current_app.logger.exception("Unhandled exception in /generic/new")
        return jsonify({"error": "Internal Server Error"}), 500
