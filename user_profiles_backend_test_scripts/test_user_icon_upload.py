import unittest
from constants import *

"""
    Request Types:
    - POST: Used to upload an image to be the group icon
        - Request:
            - Headers:
                - cookies: session_id=***
                - Content-Type: multipart/form-data
            - body: form data with icon file
                "icon":<ICON_FILE>
        - Response:
            - Status Codes:
                - 200 if image was uploaded successfully
                - 400 if image size or format was invalid
                - 401 if session_id cookie is not present or invalid
                - 500 if the database could not be reached, or file could not be saved
            - Headers:
                - Content-Type: application/json
            - body: serialized JSON in the following format
                {
                    "message":<RESULT>,
                    "icon_path":<PATH TO ICON FILE>
                }
                Where <RESULT> is a message explaining the status code to a user.
                <PATH TO ICON FILE> will be a relative path that is url-encoded in utf-8...
                    Before using the value to assemble a URI, pass the value through the decodeURI function (in javascript)
"""

class TestUserIconUpload(unittest.TestCase):

    def setUp(self):
        self.session = requests.session()
        self.session.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)
        self.larger_than_1mb_image_path = "./user_icons/larger_than_1mb.jpg"
        self.smaller_than_1mb_image_path = "./user_icons/smaller_than_1mb_image_path.jpg"

    def tearDown(self):
        self.session.close()

    # FIX
    # Unable to receive a 401 "invalid or unset session_id cookie" error

    # FIX
    # Unable to receive a 400 "request method not supported" error

    # FIX
    # Why does an invalid request method return status code 200?
    def test_invalid_request_method_should_return_status_code_400(self):
        r = self.session.post(USER_ICON_UPLOAD_URL)
        print(r.status_code)



if __name__ == "__main__":
    unittest.main()

