class Config:
    """Base config."""

    # pylint: disable=too-few-public-methods

    STATIC_FOLDER = "static"
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 3600
    QUIET = False


class ProdConfig(Config):
    """Production configuration."""

    # pylint: disable=too-few-public-methods
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    QUIET = True


class DevConfig(Config):
    """Development configuration."""

    # pylint: disable=too-few-public-methods
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""

    # pylint: disable=too-few-public-methods

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
