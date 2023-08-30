# Flask RESTful
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

# Utils
from .utils import PARTS


# Endpoint for creating an order
class Order(Resource):
    def __init__(self):
        self.post_request_parser = RequestParser()
        self.post_request_parser.add_argument('components', type=list, required=True)

    def post(self):
        # Validate request
        args = self.post_request_parser.parse_args()

        # Check if part exists
        for code in args['components']:
            if code not in PARTS:
                return {'Error': f'Part with code {code} not found'}, 404
        return args