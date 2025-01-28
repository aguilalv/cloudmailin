class Config:
    pass


class ProductionConfig(Config):
    FIRESTORE_COLLECTION = "emails"


class StagingConfig(Config):
    FIRESTORE_COLLECTION = "staging_emails"


class UnitTestingConfig(Config):
    FIRESTORE_COLLECTION = None


class FunctionalTestingConfig(Config):
    #    FIRESTORE_COLLECTION = "functional_test_emails"
    FIRESTORE_COLLECTION = None
