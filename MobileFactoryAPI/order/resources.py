# Flask RESTful
from flask_restful import Resource


# Endpoint for creating an order
class Order(Resource):
    def get(self):
        print(self)
        return 'hello world'