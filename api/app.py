# Flask
from flask import Flask

# API
from api import config


def create_app(environment):
    """
        Creates a new Flask application and initialize application.
    """

    config_map = {
        'development': config.Development(),
        'testing': config.Testing(),
        'production': config.Production(),
    }

    config_obj = config_map[environment.lower()]

    app = Flask(__name__)
    app.config.from_object(config_obj)

    return app