import unittest
from constants import *

"""
TODO
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
    pass

if __name__ == "__main__":
    unittest.main()
