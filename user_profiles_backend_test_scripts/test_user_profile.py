import unittest
import json
from constants import *

"""
Request Types:
- GET:  Get information about a user's profile
    - Request:
        - Headers:
            - cookies: session_id=***
        - URL Parameters:
            - user_id=<USER ID>
            - user=<USERNAME/EMAIL>
            - limit=<LIMIT>
              user is an optional username or email of a given user.
              user_id and user are optional.
                If neither are specified, return the profile for the current user.
                If either are specified, return the profile matching the specified user.
                If both are specified, return the profile matching the specified user_id.
              limit is the most number of groups or transactions to include in the response.
                If not included, the limit will be 5.
    - Response:
        - Status Codes:
            - 200 if current user's information was fetched correctly
            - 400 if request type was invalid or parameters were malformed
            - 401 if session_id cookie is not present or invalid
            - 404 if a user was specified and does not exist
            - 500 if the database could not be reached
        - Content-Type: application/json
        - body: serialized JSON in the following format
            {
                "message":<RESULT>,
                "user_id":<USER ID>,
                "username":<USERNAME>,
                "email":<USER EMAIL>,
                "debt":<DEBT>,
                "is_friend":<true | false>,
                "is_pending_friend":<true | false>,
                "groups":
                [
                    {
                        "group_name":<GROUP NAME>,
                        "group_id":<GROUP ID>,
                        "icon_path":<PATH TO ICON FILE>
                    },
                    ...,
                    {}
                ],
                "transactions":
                [
                    {
                        "transaction_id":<TRANSACTION ID>,
                        "name":<TRANSACTION NAME>,
                        "date":<TRANSACTION DATE>,
                        "user_debt":<USER_DEBT>,
                        "is_approved":<0|1>
                    }
                ]
            }
            <RESULT> is a message explaining the status code to a user.
            <DEBT> is the (positive) amount the current user owes the specified user,...
                or (negative) amount the specified user owes the current user.
            "groups" is a list of groups the current user has in common with the specified user.
            "transactions" is a list of most recent transactions where the current user and the specified user are both participants.
- POST: Update the current user's profile information
    - Request:
        - Headers:
            - cookies: session_id=***
        - Form Body Data:
            - username:<USERNAME>
            - email:<EMAIL>
            - password:<PASSWORD>
              At least one of the form values must be provided
    - Response:
        - Status Codes:
            - 200 if current user's information was updated correctly
            - 400 if request type was invalid or parameters were malformed
            - 401 if session_id cookie is not present or invalid
            - 500 if the database could not be reached
        - Content-Type: application/json
        - body: serialized JSON in the following format
            {
                "message":<RESULT>
            }
            <RESULT> is a message explaining the status code to a user.
"""

class TestSearchUserProfile(unittest.TestCase):

    def setUp(self):
        self.session = requests.session()
        self.session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

    def tearDown(self):
        self.session.close()

    # GET request tests

    def assertUserProfile(self, user_profile_params):
        """
        Checks that the json response to a user's profile contains the correct "username" field
        """
        user_profile = self.session.get(USER_PROFILE_URL, params=user_profile_params)
        self.assertEqual(user_profile_params["user"], user_profile.json()["username"])

    def test_matt_d_search_profile(self):
        self.assertUserProfile(MATT_D_SEARCH_PROFILE)

    def test_matt_f_search_profile(self):
        self.assertUserProfile(MATT_F_SEARCH_PROFILE)

    def test_nick_j_search_profile(self):
        self.assertUserProfile(NICK_J_SEARCH_PROFILE)

    def test_ryder_r_search_profile(self):
        self.assertUserProfile(RYDER_R_SEARCH_PROFILE)

    def test_bjtn_search_profile(self):
        self.assertUserProfile(BJTN_SEARCH_PROFILE)

    def test_non_existing_username_should_return_current_username_not_found_message(self):
        response = self.session.get(USER_PROFILE_URL, params=NON_EXISTING_USERNAME)

        json_response = response.json()

        expected_json_response = {"message": "User with username/email i_dont_exist not found"}

        self.assertEqual(json_response, expected_json_response)

    def test_non_existing_username_should_return_status_code_404(self):
        response = self.session.get(USER_PROFILE_URL, params=NON_EXISTING_USERNAME)

        status_code = response.status_code

        expected_status_code = 404

        self.assertEqual(status_code, expected_status_code)

    def test_non_existing_user_id_should_return_status_code_404(self):
        response = self.session.get(USER_PROFILE_URL, params=NON_EXISTING_USER_ID)

        status_code = response.status_code

        expected_status_code = 404

        self.assertEqual(status_code, expected_status_code)

    def test_non_existing_user_id_should_return_user_id_not_found_message(self):
        response = self.session.get(USER_PROFILE_URL, params=NON_EXISTING_USER_ID)

        json_response = response.json()

        expected_json_response = {"message": "User with user_id 69420 not found"}

        self.assertEqual(json_response, expected_json_response)

    def test_session_id_cookie_not_present_should_return_status_code_401(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE)

        status_code = response.status_code

        expected_status_code = 401

        self.assertEqual(status_code, expected_status_code)

    def test_session_id_cookie_not_present_should_return_invalid_session_id_cookie_message(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE)

        json_response = response.json()

        expected_json_response = {"message": "Invalid session_id cookie"}

        self.assertEqual(json_response, expected_json_response)

    def test_invalid_session_id_cookie_should_return_status_code_401(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE, cookies=INVALID_COOKIE)

        status_code = response.status_code
        expected_status_code = 401

        self.assertEqual(status_code, expected_status_code)

    def test_invalid_session_id_cookie_should_return_invalid_session_id_cookie_message(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE, cookies=INVALID_COOKIE)

        json_response = response.json()

        expected_json_response = {"message": "Invalid session_id cookie"}

        self.assertEqual(json_response, expected_json_response)

    def test_empty_params_should_return_status_code_200(self):
        r = self.session.get(USER_PROFILE_URL, params=EMPTY_LOGIN_PAYLOAD)

        status_code = r.status_code
        expected_status_code = 200

        self.assertEqual(status_code, expected_status_code)

    def test_empty_params_should_return_current_users_profile_in_json_response(self):
        r = self.session.get(USER_PROFILE_URL, params=EMPTY_LOGIN_PAYLOAD)

        json_response = r.json()
        expected_json_response = BJTN_USER_PROFILE

        self.assertEqual(json_response, expected_json_response)


    # POST request tests
    
    def test_invalid_session_id_should_return_invalid_session_id_cookie_message(self):
        r = requests.post(USER_PROFILE_URL, data=BJTN_LOGIN_PAYLOAD, cookies=INVALID_COOKIE)

        json_response = r.json()
        expected_json_response = {"message": "Invalid session_id cookie"}

        self.assertEqual(json_response, expected_json_response)

    def test_invalid_session_id_should_retun_status_code_401(self):
        r = requests.post(USER_PROFILE_URL, data=BJTN_LOGIN_PAYLOAD, cookies=INVALID_COOKIE)

        status_code = r.status_code
        expected_status_code = 401

        self.assertEqual(status_code, expected_status_code)

    # TODO FINISH POST tests


if __name__ == "__main__":
    unittest.main()
