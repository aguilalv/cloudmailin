class Config:
    pass


class ProductionConfig(Config):
    FIRESTORE_COLLECTION = "production_emails"


class StagingConfig(Config):
    FIRESTORE_COLLECTION = "staging_emails"


#    DEBUG = True


class UnitTestingConfig(Config):
    #    TESTING = True
    FIRESTORE_COLLECTION = None


class FunctionalTestingConfig(Config):
    #    TESTING = True
    #    FUNCTIONAL_TESTING = True
    FIRESTORE_COLLECTION = "functional_test_emails"


#    DEBUG = False
