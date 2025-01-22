import click

from flask import g, current_app
import os

from google.cloud import firestore


class DatabaseHelper:
    def __init__(self, config):
        """
        Initialize the Firestore client.
        """
        self.client = firestore.Client()
        self.config = config

        print(self.config)

        # Validate FIRESTORE_COLLECTION presence in the config
        self.collection_name = self.config.get("FIRESTORE_COLLECTION")
        if not self.collection_name:
            raise ValueError("FIRESTORE_COLLECTION is required but not configured.")

    def store_email(self, email_data):
        """
        Store an email document in the Firestore collection.
        """
        try:
            collection_name = self.collection_name
            collection = self.client.collection(collection_name)
            collection.add(email_data)
        except Exception as e:
            current_app.logger.error(
                f"Failed to store email in database: {e}", exc_info=True
            )


def get_db():
    if "db" not in g:
        g.db = DatabaseHelper(current_app.config)
        # g.db =sqlite3.connect(
        #    current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        pass
    #    db.close()


def init_db():
    """In a sql database this would clear the existing data and create new tables"""
    pass


#    db = get_db()

# with current_app.open_resource("schema.sql") as f:
#    db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """In a sql database this would clear the existing data and create new tables"""
    init_db()
    click.echo("Initialised the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
