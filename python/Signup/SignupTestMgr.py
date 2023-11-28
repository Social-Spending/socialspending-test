###############################################################
# This makes it possible to import TestMgrBase and constants.py
###############################################################
import sys
from os.path import dirname, abspath

# Get parent directory of current file (should be `/path/to/socialspendingapp-tests/python`)
parent_dir = dirname(dirname(abspath(__file__)))

# Append to sys.path to be able to import TestMgrBase and constants
sys.path.append(parent_dir)
###############################################################

from constants import *
from TestMgrBase import TestMgrBase
import requests


class SignupTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "SignupTestMgr"

    def test_post_request_to_logged_in_user(self):
        """
        POST request to signup using credentials of a user who is already logged in
        Should return:
        - 403
        - {"messsage": "User Already Logged in"}
        - No session_id
        """
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        response = session.post(SIGNUP_URL, data=BJTN_SIGNUP_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()
        session_id = response.cookies.get("session_id")

        passed = (
            status_code == 403 and
            json_response == {"message": "User Already Logged in"} and
            not session_id
        )

        session.close()

        return passed

    def test_signup_with_no_form_data(self):
        """
        POST request to signup missing user, email, and password
        Should return:
        - 400
        - {"messsage": "Form fields not found"}
        - No session_id
        """
        r = requests.post(SIGNUP_URL, data={})

        status_code = r.status_code
        json_response = r.json()
        session_id = r.cookies.get("session_id")

        passed = (
            status_code == 400 and
            json_response == {"message": "Form fields not found"} and 
            not session_id
        )

        return passed

    def test_successful_signup(self):
        """
        POST request to signup using valid username, email, and password.
        Uses the same credentials to log in and check that the user was successfully created
        """
        response = requests.post(SIGNUP_URL, data=NEW_USER_SIGNUP_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        expected_status_code = 200
        expected_json_response = {"message": "Success"}

        successful_signup = status_code == expected_status_code and json_response == expected_json_response

        # Check that we can log into new_user user
        response = requests.post(LOGIN_URL, data=NEW_USER_LOGIN_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        successful_login = status_code == expected_status_code and json_response == expected_json_response

        passed = (
            successful_signup and
            successful_login
        )

        return passed

