###############################################################
# This makes it possible to import TestMgrBase and constants.py
###############################################################
import sys
from os.path import dirname, abspath

# Get parent directory of current file
# (should be `/path/to/socialspendingapp-tests/python`)
parent_dir = dirname(dirname(abspath(__file__)))

# Append to sys.path to be able to import TestMgrBase and constants
sys.path.append(parent_dir)
###############################################################

from constants import *
from TestMgrBase import TestMgrBase
import requests


class SignoutTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "SignoutTestMgr"

    def test_successful_signout_after_loggin_in(self):
        """
        GET request to signout after logging in
        Should return:
        - 200
        - {"message": "Success"}
        - No session_id set
        """
        s = requests.session()
        login_response = s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        header = {
            "cookies": f"session_id={login_response.cookies.get('session_id')}"
        }

        signout_response = s.get(SIGNOUT_URL, headers=header)

        status_code = signout_response.status_code
        json_response = signout_response.json()
        session_id = signout_response.cookies.get("session_id")

        passed = (
            status_code == 200 and
            json_response == {"message": "Success"} and
            not session_id
        )

        return passed

    def test_successful_signout_without_loggin_in(self):
        """
        GET request to signout without logging in
        Should return:
        - 200
        - {"message": "Success"}
        - No session_id
        """
        r = requests.get(SIGNOUT_URL)

        status_code = r.status_code
        json_response = r.json()
        session_id = r.cookies.get("session_id")

        passed = (
            status_code == 200 and
            json_response == {"message": "Success"} and
            not session_id
        )

        return passed

