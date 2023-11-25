import unittest
from constants import *

"""
    Request Types:
    - GET:  Get information about the currently signed in user
        - Request:
            - Headers:
                - cookies: session_id=***
        - Response:
            - Status Codes:
                - 200 if current user's information was fetched correctly
                - 400 if request type was not GET
                - 401 if session_id cookie is not present or invalid
                - 500 if the database could not be reached
            - Content-Type:application/json
            - body: serialized JSON in the following format
                {
                    "message":<RESULT>,
                    "user_id":<USER ID>,
                    "username":<USERNAME>
                }
                <RESULT> is a message explaining the status code to a user.

"""

class TestUserInfo(unittest.TestCase):
    
    def test_get_request_fetches_correct_information(self):
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        response = session.get(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        expected_status_code = 200
        expected_json_respawn = BJTN_USER_INFO

        self.assertEqual(status_code, expected_status_code)
        self.assertEqual(json_response, expected_json_respawn)

        session.close()


    def test_invalid_request(self):
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        post_response = session.post(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        post_status_code = post_response.status_code

        head_response = session.head(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        head_status_code = head_response.status_code

        put_response = session.put(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        put_status_code = put_response.status_code

        delete_response = session.delete(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        delete_status_code = delete_response.status_code

        options_response = session.options(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        options_status_code = options_response.status_code

        # trace_response = session.trace(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        # trace_status_code = trace_response.status_code

        patch_response = session.patch(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        patch_status_code = patch_response.status_code

        expected_status_code = 400

        self.assertEqual(post_status_code, expected_status_code)
        self.assertEqual(head_status_code, expected_status_code)
        self.assertEqual(put_status_code, expected_status_code)
        self.assertEqual(delete_status_code, expected_status_code)
        self.assertEqual(options_status_code, expected_status_code)
        self.assertEqual(patch_status_code, expected_status_code)

        session.close()


    def test_get_request_invalid_session_id(self):
        response = requests.get(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        expected_status_code = 401
        expected_json_response = {"message": "Request did not include session_id cookie"}

        self.assertEqual(status_code, expected_status_code)
        self.assertEqual(json_response, expected_json_response)


if __name__ == "__main__":
    unittest.main()
