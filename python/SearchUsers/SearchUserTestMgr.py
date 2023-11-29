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

class SearchUsersTestMgr(TestMgrBase):
    def setup(self):
        self.test_name = "SearchUsersTestMgr"

    def test_valid_search_returns_matching_usernames(self):
        s = requests.session()

        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        r = s.post(SEARCH_USERS_URL, json={"search_term": "Va"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 200 and
            json_response == {'message': 'Success', 'users': [{'user_id': 3, 'username': 'Vanquisher'}, {'user_id': 4, 'username': 'Vasagle'}]}
        )

        s.close()
        
        return passed

    def test_invalid_request_method(self):
        s = requests.session()

        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        r = s.get(SEARCH_USERS_URL, json={"search_term": "Va"})

        status_code = r.status_code

        passed = (
            status_code == 400
        )

        s.close()

        return passed

    def test_invalid_session_id_cookie(self):
        # FIX
        # This always returns a 500 erorr "unable to contatc database" if session_id cookie is not present or invalid
        header = {
            "cookies": f"session_id={INVALID_COOKIE.get('session_id')}"
        }

        r = requests.post(SEARCH_USERS_URL, json={"search_term": "Va"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 401
        )

        if not passed:
            print(f"SearchUsersTestMgr.{self.test_invalid_session_id_cookie.__name__}():\nStatus code: {status_code}\nJson response:{json_response}")

        return passed
