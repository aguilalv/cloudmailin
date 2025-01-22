import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-really-needs-to-be-changed")
    FIRESTORE_COLLECTION = "emails"


class ProductionConfig(Config):
    DEBUG = False


# class StagingConfig(Config):
#     DEBUG = True
#     DEVELOPMENT = True
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#     DEVELOPMENT = True
#
class UnitTestingConfig(Config):
    TESTING = True
    UNIT_TESTING = True
    DEBUG = False
