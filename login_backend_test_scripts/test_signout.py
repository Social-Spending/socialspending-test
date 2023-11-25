import unittest
import requests
from constants import *

"""
Signs the user out
- Request:
    - Headers:
        - cookies: session_id=***
- Response:
    - Status Codes:
        - 200 if user was correctly signed out, or was never signed in
        - 500 if the database could not be reached
    - Content-Type:application/json
    - body: serialized JSON in the following format
        {
            "message":<RESULT>
        }
        <RESULT> is a message explaining the status code to a user.
"""

class TestSignout(unittest.TestCase):
    
    def test_signout_with_valid_session_id_cookie(self):
        response = requests.get(SIGNOUT_URL, data=BJTN_LOGIN_PAYLOAD, cookies=GET_VALID_COOKIES())

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 200
        expected_json_response = {"message": "Success"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))


    def test_signout_with_no_session_id_cookie(self):
        response = requests.get(SIGNOUT_URL, data=BJTN_LOGIN_PAYLOAD)

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 200
        expected_json_response = {"message": "Success"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))




if __name__ == "__main__":
    unittest.main()

