# Flask RESTful
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

# Utils
from .utils import PARTS

# uuid
import uuid

# datetime
from datetime import datetime


# Endpoint for creating an order
class Order(Resource):

    def __init__(self):
        self.post_request_parser = RequestParser()
        self.post_request_parser.add_argument('components', type=list, location='json', required=True)


    # To generate a unique order ID, we can use a combination of a timestamp and a random number.
    def generate_order_id(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_number = str(uuid.uuid4().int)[:10]
        order_id = f"{timestamp}_{random_number}"
        return order_id


    def post(self):
        # Validate request
        args = self.post_request_parser.parse_args()

        components = args['components']

        # Validate parts list. This will allow us to avoid iterating through a massive components list.
        if len(components) > len(PARTS):
            return {'Error': 'Invalid request'}, 400

        # Define the response
        response = {
            'order_id': self.generate_order_id(),
            'total': 0.0,
            'parts': []
        }

        # Construct the response
        for code in sorted(components):    
            # Check if part exist in the dictionary.
            if code not in PARTS:
                return {'Error': f'Part with code {code} not found'}, 404
            part = PARTS[code]
            response['total'] += part['price']
            response['parts'].append(part['part'])
        
        return response, 201