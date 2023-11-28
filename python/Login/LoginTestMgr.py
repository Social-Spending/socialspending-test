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


class LoginTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "LoginTestMgr"

    def _make_get_request_to_login(self, payload, cookie):
        """
        Helper method to make a GET request to login and extract status code, json response, and session_id.
        """
        r = requests.get(LOGIN_URL, data=payload, cookies=cookie)
        return (
            r.status_code,
            r.json(),
            r.cookies.get("session_id")
        )

    def _make_post_request_to_login(self, payload):
        """
        Helper method to make a POST request to login and extract status code, json response, and session_id.
        """
        r = requests.post(LOGIN_URL, data=payload)
        return (
            r.status_code,
            r.json(),
            r.cookies.get("session_id")
        )

    def test_successful_login_with_valid_username_and_password(self):
        """
        POST request to login with valid username and password
        Login is successful if:
        - Status code = 200
        - JSON response = {"message": "Success"}
        - session_id cookie was set
        """
        status_code, json_response, session_id = self._make_post_request_to_login(payload=BJTN_LOGIN_PAYLOAD)

        passed = (
                status_code == 200 and
                json_response == {"message": "Success"} and
                session_id
        )

        return passed

    def test_unsuccessful_login_without_username_and_password(self):
        """
        POST request to login with no username and password
        Should return:
        - 400
        - {"message": "Form fields not found"}
        - No session_id cookie
        """
        status_code, json_response, session_id = self._make_post_request_to_login(payload=EMPTY_LOGIN_PAYLOAD)

        passed = (
                status_code == 400 and
                json_response == {"message": "Form fields not found"} and
                not session_id
        )

        return passed

    def test_unsuccessful_login_with_invalid_username_and_password(self):
        """
        POST request with non existing username and password
        Should return:
        - 401
        - {"message": "Invalid username and/or password"}
        - No session_id cookie
        """
        status_code, json_response, session_id = self._make_post_request_to_login(
            payload=NON_EXISTING_USER_LOGIN_PAYLOAD)

        passed = (
                status_code == 401 and
                json_response == {"message": "Invalid username and/or password"} and
                not session_id
        )

        return passed

    def test_unsuccessful_login_with_empty_cookie(self):
        """
        GET request to login with no session_id
        Should return:
        - 401
        - {"message": "Invalid session_id cookie or cookie not present"}
        - No session_id
        """

        status_code, json_response, session_id = self._make_get_request_to_login(payload=BJTN_LOGIN_PAYLOAD, cookie={})

        passed = (
                status_code == 401 and
                json_response == {"message": "Invalid session_id cookie or cookie not present"} and
                not session_id
        )

        return passed

    def test_unsuccessful_login_with_invalid_cookie(self):
        """
        GET request to login with sessino_id = -1
        Should return:
        - 401
        - {"message": "Invalid session_id cookie or cookie not present"}
        - No session_id
        """

        status_code, json_response, session_id = self._make_get_request_to_login(payload=BJTN_LOGIN_PAYLOAD,
                                                                                 cookie=INVALID_COOKIE)

        passed = (
                status_code == 401 and
                json_response == {"message": "Invalid session_id cookie or cookie not present"} and
                not session_id
        )

        return passed
