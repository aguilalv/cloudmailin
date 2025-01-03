import os
import logging
from flask import Flask, request

from cloudmailin.handler_registry import HANDLERS_MAP, HandlerRegistry


def create_app(test_config=None):
    # Late import to ensure the function is patched correctly in tests.
    # This follows Flask's pattern of initializing dependencies dynamically within create_app,
    # and avoids module-level imports that can cause issues with testing and state management.
    from .handler_registry import initialize_handler_registry_from_config

    from .logging_setup import configure_logging  # Import the logging setup

    # Create the app
    app = Flask(__name__, instance_relative_config=True)

    # Configure Logging
    configure_logging()
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
    from . import generic

    app.register_blueprint(generic.bp)

    return app
