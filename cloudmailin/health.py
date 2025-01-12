from flask import Blueprint, jsonify
import os

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.route("/", methods=["GET"])
def health_check():
    """
    A health check endpoint to verify the service's status.
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "version": os.getenv("APP_VERSION", "unknown"),
                "deployed_at": os.getenv("DEPLOYED_AT", "unknown"),
            }
        ),
        200,
    )
