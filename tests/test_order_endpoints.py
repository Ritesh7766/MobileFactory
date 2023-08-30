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


    def check_valid_requests(self, parts, data):
        # Check total value of parts and parts list.
        total, parts_list = 0.0, []
        for code in parts:
            part = PARTS[code]
            total += part["price"]
            parts_list.append(part["part"])

        self.assertListEqual(parts_list, data["parts"])
        self.assertEqual(total, data["total"])


    def test_all_combinations(self):
        order_ids = set()
        # Try every possible combination of requests.
        for i in range(1, len(PARTS) + 1):
            for parts in itertools.combinations(PARTS, i):
                response = self.app.post("/order", json={"components": parts})
                data = json.loads(response.data)

                # Check successful order creations
                if response.status_code == 201:
                    self.check_valid_requests(parts=parts, data=data)

                    # Make sure every order_id is unique.
                    self.assertNotIn(data["order_id"], order_ids)
                    order_ids.add(data["order_id"])
                    continue

                # Check bad requests
                self.assertEqual(response.status_code, 400)
                





if __name__ == "__main__":
    unittest.main()