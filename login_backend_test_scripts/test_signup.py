import unittest
from constants import *

"""
    Request Types:
    - POST: Create a new user, if the username and email were not already found
        - Request Form Data:
            - 'user': username of the new user
            - 'email': email of the new user
            - 'password': password of the new user
        - Response:
            - Status Codes:
                - 200 if user was created successfully
                - 403 if user is already logged in
                - 400 if form data is not present
                - 500 if the database could not be reached
            - Content-Type:application/json
            - body: serialized JSON in the following format
                    {
                        'message':<RESULT>
                    }
                    Where <RESULT> is a message explaining the status code to a user

"""

class TestSignup(unittest.TestCase):
    def test_signup_post_request_successful_signup(self):
        # NOTE
        # This should only be run on localhost
        signup_url = "https://localhost/signup.php"
        login_url = "https://localhost.login.php"

        try:
            if signup_url == SIGNUP_URL:
                raise requests.exceptions.InvalidURL()
            response = requests.post(signup_url, data=NEW_USER_SIGNUP_PAYLOAD)

            status_code = response.status_code
            json_response = response.json()

            expected_status_code = 200
            expected_json_response = {"message": "Success"}

            successful_signup = status_code == expected_status_code and json_response == expected_json_response

            # Check that we can log into new_user user
            response = requests.post(login_url, data=NEW_USER_LOGIN_PAYLOAD)

            status_code = response.status_code
            json_response = response.json()

            successful_login = status_code == expected_status_code and json_response == expected_json_response

            self.assertTrue(successful_signup)
            self.assertTrue(successful_login)

        except requests.exceptions.ConnectionError:
            print(f"Unable to connect to localhost. Did you forget to turn on local server before running \"test_signup_post_request_successful_signup()\" from \"test_signup.py?\"")
        except requests.exceptions.InvalidURL:
            print(f"Aborting... Trying to run \"test_signup_post_request_successful_signup()\" on something other than \"https://localhost/signup.php\"")


    def test_signup_post_request_already_logged_in_user(self):
        session = requests.session()

        session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        response = session.post(SIGNUP_URL, data=BJTN_SIGNUP_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        expected_status_code = 403
        expected_json_response = {"message": "User Already Logged in"}

        self.assertEqual(status_code, expected_status_code)
        self.assertEqual(json_response, expected_json_response)

        session.close()


    def test_signup_post_request_form_data_not_present(self):
        response = requests.post(SIGNUP_URL, data=EMPTY_SIGNUP_PAYLOAD)

        status_code = response.status_code
        json_response = response.json()

        expected_status_code = 400
        expected_json_response = {"message": "Form fields not found"}

        self.assertEqual(status_code, expected_status_code)
        self.assertEqual(json_response, expected_json_response)


if __name__ == "__main__":
    unittest.main()
