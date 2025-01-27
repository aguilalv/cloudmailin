from flask import Flask, request, g
import logging
import json
from datetime import datetime, UTC
import os


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
    # Load environment-specific configuration (ProductionConfig is the default)
    env_config = os.getenv("FLASK_ENV", "ProductionConfig")
    try:
        app.config.from_object(f"cloudmailin.config.{env_config}")
    except ImportError:
        # Fallback to ProductionConfig if FLASK_ENV is invalid
        app.config.from_object("cloudmailin.config.ProductionConfig")
    # Override default configuration if a test configuration or an enviromnet variable
    if test_config:
        # Override with test configuration
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

    @app.before_request
    def set_firestore_collection():
        """
        Check for a custom Firestore collection in the request headers.
        Set it in g if present.
        """
        custom_collection = request.headers.get("X-Firestore-Collection",None)
        if custom_collection:
            g.firestore_collection = custom_collection
            app.logger.info(f"Overriding Firestore collection to: {custom_collection}")

    # Register Blueprints
    from . import generic, health

    app.register_blueprint(generic.bp)
    app.register_blueprint(health.bp)

    return app
