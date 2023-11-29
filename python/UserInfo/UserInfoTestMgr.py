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

class UserInfoTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "UserInfoTestMgr"

    def test_valid_search_fetches_correct_information(self):
        s = requests.session()

        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        r = s.get(USER_INFO_URL)

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 200 and
            json_response == {'user_id': 5, 'username': 'level_five_yeti', 'message': 'Success'}
        )

        s.close()

        return passed

    def test_invalid_request_methods(self):
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        post_response = session.post(USER_INFO_URL)
        post_status_code = post_response.status_code

        head_response = session.head(USER_INFO_URL)
        head_status_code = head_response.status_code

        put_response = session.put(USER_INFO_URL)
        put_status_code = put_response.status_code

        delete_response = session.delete(USER_INFO_URL)
        delete_status_code = delete_response.status_code

        options_response = session.options(USER_INFO_URL)
        options_status_code = options_response.status_code

        # trace_response = session.trace(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        # trace_status_code = trace_response.status_code

        patch_response = session.patch(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        patch_status_code = patch_response.status_code

        passed = (
            post_status_code == 400 and
            head_status_code == 400 and
            put_status_code == 400 and
            delete_status_code == 400 and
            options_status_code == 400 and
            patch_status_code == 400
        )

        session.close()

        return passed


    def test_invalid_session_id(self):
        header = {
            "cookies": f"session_id={INVALID_COOKIE.get('session_id')}"
        }

        r = requests.get(USER_INFO_URL, headers=header)

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 401 and
            json_response == {"message": "Request did not include session_id cookie"}
        )

        return passed
