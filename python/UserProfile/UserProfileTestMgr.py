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

class UserProfileTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "UserProfileTestMgr"

    def test_get_request_fetches_correct_user_information(self):
        """
        GET request to user_profile.php with params = {"user_id": 1, "user": "Roasted715Jr"}
        """
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)
        user_profile = s.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE)
        status_code = user_profile.status_code

        passed = (
            user_profile.json()["username"] == MATT_D_SEARCH_PROFILE["user"] and
            status_code == 200
        )
        s.close()
        return passed

    def test_non_existing_username_profile(self):
        """
        GET request to user_profile.php with params = {"user": "i_dont_exist"}
        """
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)
        r = s.get(USER_PROFILE_URL, params=NON_EXISTING_USERNAME)

        json_response = r.json()
        status_code = r.status_code

        passed = (
            status_code == 404 and
            json_response == {"message": "User with username/email i_dont_exist not found"}
        )
        s.close()
        return passed

    def test_non_existing_user_id_profile(self):
        """
        GET request to user_profile.php with params = {"user_id": 69420}
        """
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)
        r = s.get(USER_PROFILE_URL, params=NON_EXISTING_USER_ID)

        json_response = r.json()
        status_code = r.status_code

        passed = (
            status_code == 404 and
            json_response == {"message": "User with user_id 69420 not found"}               
        )
        s.close()
        return passed

    def test_absent_session_id_cookie(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE)

        status_code = response.status_code
        json_response = response.json()

        passed = (
            status_code == 401 and
            json_response == {"message": "Invalid session_id cookie"}
        )

        return passed

    def test_invalid_session_id_cookie(self):
        response = requests.get(USER_PROFILE_URL, params=MATT_D_SEARCH_PROFILE, cookies=INVALID_COOKIE)

        status_code = response.status_code
        json_response = response.json()

        passed = (
            status_code == 401 and
            json_response == {"message": "Invalid session_id cookie"}
        )
        
        if passed:
            print("POG")

        return passed

    def test_empty_params(self):
        """
        GET request to user_profile with empty params should return currently logged in user's profile
        """
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)
        r = s.get(USER_PROFILE_URL, params={})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 200 and
            json_response == BJTN_USER_PROFILE
        )

        s.close()
        return passed

    def test_successful_profile_update(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        new_profile_payload = {
            "username": "level_one_yeti",
            "email": "level_one_yeti@clashofclans.com",
        }

        old_profile_payload = {
            "username": "level_five_yeti",
            "email": "BJTNoguera@socialspendingapp.com"
        }

        old_username = s.get(USER_PROFILE_URL, data=BJTN_SEARCH_PROFILE).json().get("username")
        old_email = s.get(USER_PROFILE_URL, data=BJTN_SEARCH_PROFILE).json().get("email")

        r = s.post(USER_PROFILE_URL, data=new_profile_payload)

        status_code = r.status_code

        new_username = s.get(USER_PROFILE_URL, data=BJTN_SEARCH_PROFILE).json().get("username")
        new_email = s.get(USER_PROFILE_URL, data=BJTN_SEARCH_PROFILE).json().get("email")

        # This reverses the email and username change
        s.post(USER_PROFILE_URL, data=old_profile_payload)

        passed = (
            old_email != new_email and
            old_username != new_username and
            status_code == 200
        )
        
        s.close()
        return passed

    def test_update_to_invalid_username(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_TEST_LOGIN_PAYLOAD)

        r = s.post(USER_PROFILE_URL, params={"username": "abc"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 400 and
            json_response == {"message": "Username is invalid"}
        )
        s.close()
        return passed

    def test_update_to_invalid_email(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_TEST_LOGIN_PAYLOAD)

        r = s.post(USER_PROFILE_URL, params={"email": "not_an_email"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 400 and
            json_response == {"message": "Email is invalid"}
        )
        s.close()
        return passed

    def test_update_to_existing_username(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_TEST_LOGIN_PAYLOAD)

        r = s.post(USER_PROFILE_URL, params={"username": "level_five_yeti"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 400 and
            json_response == {"message": "An account with that username already exists"}
        )
        s.close()
        return passed

    def test_update_to_existing_email(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_TEST_LOGIN_PAYLOAD)

        r = s.post(USER_PROFILE_URL, params={"email": "BJTNoguera@socialspendingapp.com"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 400 and
            json_response == {"message": "An account with that email already exists"}
        )
        s.close()
        return passed

    def test_update_to_invalid_password(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_TEST_LOGIN_PAYLOAD)

        r = s.post(USER_PROFILE_URL, params={"password": "pass"})

        status_code = r.status_code
        json_response = r.json()

        passed = (
            status_code == 400 and
            json_response == {"message": "Password is invalid"}
        )
        s.close()
        return passed

    def test_invalid_request_method(self):
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        post_response = session.post(USER_PROFILE_URL)
        post_status_code = post_response.status_code

        head_response = session.head(USER_PROFILE_URL)
        head_status_code = head_response.status_code

        put_response = session.put(USER_PROFILE_URL)
        put_status_code = put_response.status_code

        delete_response = session.delete(USER_PROFILE_URL)
        delete_status_code = delete_response.status_code

        options_response = session.options(USER_PROFILE_URL)
        options_status_code = options_response.status_code

        # trace_response = session.trace(USER_INFO_URL, data=BJTN_LOGIN_PAYLOAD)
        # trace_status_code = trace_response.status_code

        patch_response = session.patch(USER_PROFILE_URL, data=BJTN_LOGIN_PAYLOAD)
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
