import os

class Config:
    DEBUG = False
    TESTING = False
    FUNCTIONAL_TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-really-needs-to-be-changed")


class ProductionConfig(Config):
    FIRESTORE_COLLECTION = "production_emails"


class StagingConfig(Config):
    FIRESTORE_COLLECTION = "staging_emails"
    DEBUG = True


class UnitTestingConfig(Config):
    TESTING = True
    FIRESTORE_COLLECTION = None


class FunctionalTestingConfig(Config):
    FUNCTIONAL_TESTING = True
    FIRESTORE_COLLECTION = "functional_test_emails"

