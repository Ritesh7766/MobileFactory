# Flask
from flask import Flask

# Flask RESTful
from flask_restful import Api

# API
from MobileFactoryAPI import config
from MobileFactoryAPI.order import resources


def create_app():
    """
        Creates a new Flask application and initialize application.
    """

    app = Flask(__name__)
    app.config.from_object(config.Config)

    api = Api(app)
    api.add_resource(resources.Order, '/order')

    return app