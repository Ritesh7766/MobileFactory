# Flask RESTful
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

# Utils
from .utils import PARTS

# uuid
import uuid

# datetime
from datetime import datetime

# defaulidict
from collections import defaultdict

# Endpoint for creating an order
class Order(Resource):

    def __init__(self):
        self.post_request_parser = RequestParser()
        self.post_request_parser.add_argument('components', type=list, location='json', required=True)


    def validate_post_request(self, components):
        errors = defaultdict(list)

        # Check list size before hand to avoid iterating through a large list.
        if len(components) > 5:
            errors['Invalid Request'].append('You only need to specify 5 components')
            return errors

        component_types = set()
        for code in components:
            # Check if part exist in the dictionary.
            if code not in PARTS:
                errors['Invalid Codes'].append(f'Part with code {code} does not exists')
                continue
            
            part = PARTS[code]

            # Check if same component type has been specified multiple times.
            if part['type'] in component_types:
                errors['Same Component Types'].append(f'{part["type"]} type specified multiple times')
            component_types.add(part['type'])
        
        # Check for missing parts
        missing_components = {'Screen', 'Camera', 'OS', 'Port', 'Body'} - component_types
        if missing_components:
            errors['Missing Components'] = list(missing_components)

        return errors


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

        errors = self.validate_post_request(components)
        if errors:
            return errors, 400

        # Define the response
        response = {
            'order_id': self.generate_order_id(),
            'total': 0.0,
            'parts': []
        }
 
        # Construct the response
        component_types = set()
        for code in sorted(components):    
            part = PARTS[code]
            response['total'] += part['price']
            response['parts'].append(part['part'])

        return response, 201