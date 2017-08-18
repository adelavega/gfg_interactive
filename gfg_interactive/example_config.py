import os

class Config(object):
    #### User-specified settings for talking to services: must configure these!
    SECRET_KEY = 'enter key here' # Must match the MODULE_INTEGRATION_KEY of genesforgood PHP app configuration
    SQLALCHEMY_DATABASE_URI = "??"

    # FIXME: In practice, all of our servers hardcode username:password@host:port credentials into the host URL too (redundant)
    RESEARCH_DB_HOST = None  # e.g. localhost on dev server
    RESEARCH_DB_NAME = None # eg `gfg_research`
    RESEARCH_DB_USER = None
    RESEARCH_DB_PASSWORD = None

    # Whether to enable "development debug mode", which allows experiments to be retaken + longer delay intervals
    EXP_DEBUG = False
    DEVELOPMENT = False  # Possibly unused legacy setting?

    #### Settings required to operate flask app and addons
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    ## TODO: Default setting will suppress log warnings in minimally invasive fashion.
    #   If we are confident no signals are used, better to switch to `False`.
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """To be used on web-facing servers. Customize with secret key + DB credentials as needed."""
    DEBUG = False

    SECRET_KEY = 'enter key here' # Must match the MODULE_INTEGRATION_KEY of genesforgood PHP app configuration
    SQLALCHEMY_DATABASE_URI = "??"

    # FIXME: In practice, all of our servers hardcode username:password@host:port credentials into the host URL too (redundant)
    RESEARCH_DB_HOST = "??"  # e.g. localhost on dev server
    RESEARCH_DB_NAME = "??" # eg `gfg_research`
    RESEARCH_DB_USER = "??"
    RESEARCH_DB_PASSWORD = "??"


class DevelopmentConfig(Config):
    """
    Support development/debugging of experiments; generally for use when running locally.
    """
    DEVELOPMENT = True
    DEBUG = True
    EXP_DEBUG = True


class ScriptConfig(Config):
    """
    Recommended settings for running manage.py scripts

    Migrations scripts may require higher DB permissions than are granted to the regular app DB user
    """
    # FIXME: In practice, all of our servers hardcode username:password@host:port credentials into the host URL too (redundant)
    RESEARCH_DB_HOST = None  # e.g. localhost on dev server
    RESEARCH_DB_NAME = None # eg `gfg_research`
    RESEARCH_DB_USER = 'rootuser'
    RESEARCH_DB_PASSWORD = 'insert correct password here'