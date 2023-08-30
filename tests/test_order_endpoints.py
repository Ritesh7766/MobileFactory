# unitest
import unittest

# Get app instance
import os
os.chdir('..')
from app import app

# flask
from flask import json

# itertools
import itertools

# Get the database
from MobileFactoryAPI.order.utils import PARTS


class TestOrderEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        

    def test_successful_order_creation(self):
        order_ids = set()
        # Try every possible combination of requests.
        for i in range(1, len(PARTS) + 1):
            for parts in itertools.combinations(PARTS, i):
                response = self.app.post("/order", json={"components": parts})
                data = json.loads(response.data)

                # Check status code.
                self.assertEqual(response.status_code, 201)

                # Check total value of parts and parts list.
                total, parts_list = 0.0, []
                for code in parts:
                    part = PARTS[code]
                    total += part["price"]
                    parts_list.append(part["part"])

                self.assertListEqual(parts_list, data["parts"])
                self.assertEqual(data["total"], total)

                # Make sure every order_id is unique.
                self.assertNotIn(data["order_id"], order_ids)
                order_ids.add(data["order_id"])


    def test_invalid_components(self):
        response = self.app.post("/order", json={ "components": ["I", "A", "D", "F", "K", "Z"] })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Part with code Z not found", data["Error"])

    
    def test_large_payload(self):
        response = self.app.post("/order", json={ "components": list(range(2 ** 15) ) })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        

if __name__ == "__main__":
    unittest.main()