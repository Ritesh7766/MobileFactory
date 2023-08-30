# Flask RESTful
from flask_restful import Resource

# Flask
from flask import request


# Endpoint for creating an order
class Order(Resource):
    def post(self):
        return 'hello world'