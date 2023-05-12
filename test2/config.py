# config.py

class Config:
    # common configuration values
    SECRET_KEY = "some-secret-key"
    DEBUG = False

class DevelopmentConfig(Config):
    # configuration values for development environment
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"

class TestingConfig(Config):
    # configuration values for testing environment
    TESTING = True
    DATABASE_URI = "sqlite:///test.db"

class ProductionConfig(Config):
    # configuration values for production environment
    DATABASE_URI = "postgresql://user:password@host/database"

# a dictionary to map the environment name to the config class
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
