# from pathlib import Path
# import tempfile

import pytest
from cloudmailin import create_app
from cloudmailin.db import get_db, init_db

# test_db_file = Path(__file__) / "data.sql"
# with open(test_db_file)


@pytest.fixture
def app():
    #    db_fd, db_path = tempfile.mkstemp(

    app = create_app({"TESTING": True})

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
