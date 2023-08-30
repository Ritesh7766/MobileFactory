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


    def validate_post_request(self, components):
        errors = {}

        # Pre-check the size of the list to avoid iterating through a lengthy collection beforehand.
        if len(components) > 5:
            errors['Invalid Request'] = 'You only need to specify 5 components'
            return errors

        specified_component_types, invalid_codes, repeated_component_types = set(), set(), set()
        for code in components:
            # Validate code.
            if code not in PARTS:
                invalid_codes.add(code)
                continue

            part = PARTS[code]

            # Confirm whether the same component type has been provided more than once.
            if part['type'] in specified_component_types:
                repeated_component_types.add(part["type"])
            specified_component_types.add(part['type'])
        
        # Check for missing components
        missing_components = {'Screen', 'Camera', 'OS', 'Port', 'Body'} - specified_component_types
        if missing_components:
            errors['Missing Components'] = list(missing_components)

        if invalid_codes:
            errors['Invalid Codes'] = list(invalid_codes)
        
        if repeated_component_types:
            errors['Repeated Component Types'] = list(repeated_component_types)

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

        # Initialize the response dict
        response = {
            'order_id': self.generate_order_id(),
            'total': 0.0,
            'parts': []
        }
 
        # Construct the response
        for code in sorted(components):    
            part = PARTS[code]
            response['total'] += part['price']
            response['parts'].append(part['part'])

        return response, 201