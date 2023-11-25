import unittest
import requests
from constants import *

"""
Request Types:
- GET:  Can be used to check if the user's existing session_id cookie is authenticated,
        without providing credentials to do authentication
    - Response:
        - Status Codes:
            - 200 if the session_id cookie is authenticated
            - 401 if the session_id cookie is not set, or is set but not valid
            - 500 if the database could not be reached
        - Content-Type: application/json
        - body: serialized JSON in the following format
                {
                    "message":<RESULT>
                }
                Where <RESULT> is a message explaining the status code to a user

- POST: Check if a user's existing session_id cookie is authenticated,
        and if not, use provided form data to attempt authentication.
        If authentication is correct, a 'session_id' cookie is set in the response
    - Request Form Data:
        - 'user': username or email of the credentialed user
        - 'password': password of the credentialed user
    - Response:
        - Status Codes:
            - 200 if authentication is successful
            - 401 if provided credentials are invalid
            - 400 if form data is not present
            - 500 if the database could not be reached
        - Content-Type: application/json
        - body: serialized JSON in the following format
                {
                    "message":<RESULT>
                }
                Where <RESULT> is a message explaining the status code to a user
"""

class TestLogin(unittest.TestCase):


    def test_login_get_request_with_authenticated_cookie(self):
        response = requests.get(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD, cookies=GET_VALID_COOKIES())

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 200
        expected_json_response = {"message": "Success"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))


    def test_login_get_request_with_invalid_cookie(self):
        response = requests.get(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 401
        expected_json_response = {"message": "Invalid session_id cookie or cookie not present"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))


    def test_login_post_request_with_valid_username_and_password(self):
        response = requests.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 200
        expected_json_response = {"message": "Success"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNotNone(response.cookies.get("session_id"))


    def test_login_post_request_with_invalid_username_and_password(self):
        response = requests.post(LOGIN_URL, data=NON_EXISTING_USER_LOGIN_PAYLOAD)

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 401
        expected_json_response = {"message": "Invalid username and/or password"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))


    def test_login_post_request_without_form_data(self):
        response = requests.post(LOGIN_URL, data=EMPTY_LOGIN_PAYLOAD)

        actual_status_code = response.status_code
        actual_json_response = response.json()

        expected_status_code = 400
        expected_json_response = {"message": "Form fields not found"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_json_response, expected_json_response)
        self.assertIsNone(response.cookies.get("session_id"))


if __name__ == "__main__":
    unittest.main()
