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

# Images obtained from https://freetestdata.com/
LARGER_THAN_1MB_IMG = "./5mb.png"
SVG_IMG = "./501kb.svg"
VALID_PNG = "./500kb.png"
VALID_JPEG = "./128kb.jpg"
VALID_GIF = "./431kb.gif"

class UserIconeUploadTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "UserIconeUploadTestMgr"

    def test_invalid_request_type(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(VALID_PNG, "rb")}

        r = s.get(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 400 and
            json_response == "Request method not supported"
        )
        s.close()

        return passed

    def test_upload_valid_png(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(VALID_PNG, "rb")}

        r = s.post(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 200 and
            json_response == "Success"
        )
        s.close()

        return passed

    def test_upload_valid_jpeg(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(VALID_JPEG, "rb")}

        r = s.post(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 200 and
            json_response == "Success"
        )
        s.close()

        return passed

    def test_upload_valid_gif(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(VALID_GIF, "rb")}

        r = s.post(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 200 and
            json_response == "Success"
        )
        s.close()

        return passed

    def test_upload_invalid_img_type(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(SVG_IMG, "rb")}

        r = s.post(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 400 and
            json_response == "Image is not valid image type. Must be gif, png, or jpeg"
        )
        s.close()

        return passed

    def test_invalid_image_size(self):
        s = requests.session()
        s.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

        form_data = {"icon": open(LARGER_THAN_1MB_IMG, "rb")}

        r = s.post(USER_ICON_UPLOAD_URL, files=form_data)

        status_code = r.status_code
        json_response = r.json().get("message")

        passed = (
            status_code == 400 and
            json_response == "Cannot upload images exceeding 2048 bytes"
        )
        s.close()

        return passed

