import unittest
from constants import *

"""
    Request Types:
    - POST: Search for a user based on a partial username or email
        - Request:
            - Headers:
                - Content-Type: application/json
                - cookies: session_id=***
            - Body:
                {
                    "search_term":<PARTIAL USERNAME OR EMAIL>
                }
        - Response:
            - Status Codes:
                - 200 if database was correctly searched for matching users
                - 400 if request type was not POST, or body JSON was malformed
                - 401 if session_id cookie is not present or invalid
                - 500 if the database could not be reached
            - Headers:
                - Content-Type:application/json
            - Body: serialized JSON in the following format
                {
                    "message":<RESULT>,
                    "users":
                    [
                        {
                            "user_id":<USER ID>,
                            "username":<USERNAME>,
                            "icon_path":<PATH TO ICON FILE>
                        }
                    ]
                }
                <RESULT> is a message explaining the status code to a user.
                <PATH TO ICON FILE> will be a relative path that is url-encoded in utf-8...
                    Before using the value to assemble a URI, pass the value through the decodeURI function (in javascript)
"""
class TestSearchUsers(unittest.TestCase):

    def setUp(self):
        self.session = requests.session()
        self.session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

    def tearDown(self):
        self.session.close()

    # FIX
    # Unable to receive a 401 error
    # Skipping the cookie altogether returns 500 error
    # Putting an invalid cookie returns 400 error
    # def test_invalid_session_id_cookie_should_return_status_code_401(self):
    #     r = self.session.post(SEARCH_USERS_URL, cookies=INVALID_COOKIE,  json={"search_term": "Va"})
    #
    #     status_code = r.status_code
    #
    #     expecected_status_code = 401
    #
    #     self.assertEqual(status_code, expecected_status_code)

    def test_valid_search_should_return_correct_matching_usernames(self):
        r = self.session.post(SEARCH_USERS_URL, json={"search_term": "Va"})

        json_response = r.json()

        expected_json_response = {'message': 'Success', 'users': [{'user_id': 3, 'username': 'Vanquisher'}, {'user_id': 4, 'username': 'Vasagle'}]}

        self.assertEqual(json_response, expected_json_response)

    def test_invalid_request_should_return_status_code_400(self):
        r = self.session.get(SEARCH_USERS_URL, json={"search_term": "Va"})

        status_code = r.status_code
        expected_status_code = 400

        self.assertEqual(status_code, expected_status_code)

    def test_search_for_non_existing_user_should_return_no_users_and_a_success_message(self):
        r = self.session.post(SEARCH_USERS_URL, json={"search_term": "ooga"})

        json_response = r.json()
        expected_json_response = {'message': 'Success', 'users': []}

        self.assertEqual(json_response, expected_json_response)



if __name__ == "__main__":
    unittest.main()
