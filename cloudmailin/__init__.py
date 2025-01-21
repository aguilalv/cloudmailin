from flask import Flask, request
import logging
import json
from datetime import datetime, UTC


class JSONFormatter(logging.Formatter):
    """
    Custom JSON log formatter for structured logs.
    """

    def format(self, record):
        log_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

def create_app(test_config=None):
    # Late import to ensure the function is patched correctly in tests.
    # Follows Flask's pattern of initializing dependencies dynamically within create_app
    # Avoids module-level imports that can cause issues with testing and state mgmnt
    from .handler_registry import initialize_handler_registry_from_config

    # Create the app
    app = Flask(__name__, instance_relative_config=True)

    # Configure Logging
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    app_logger = logging.getLogger("cloudmailin")
    app_logger.setLevel(logging.INFO)
    app_logger.handlers = [handler]
    app_logger.propagate = True  # Ensure logs propagate to the root logger

    # Attach the app logger to Flask's logger
    app.logger.handlers = app_logger.handlers
    app.logger.setLevel(app_logger.level)
    app.logger.propagate = True

    app.logger.info("Application starting...")

    # App Configuration
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Initialize and add handler registry to the app
    config_path = app.config.get("HANDLER_CONFIG_PATH", "config/handler_config.yaml")

    app.config["handler_registry"] = initialize_handler_registry_from_config(
        config_path
    )

    # Initialize Database
    from . import db

    db.init_app(app)

    # Setup logging before every request
    @app.before_request
    def log_incoming_request():
        """
        Log details of each incoming request.
        """
        app.logger.info(f"Received request: {request.method} {request.path}")

    # Register Blueprints
    from . import generic, health

    app.register_blueprint(generic.bp)
    app.register_blueprint(health.bp)

    return app
