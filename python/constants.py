import requests

LOCALHOST = "http://localhost"
DEPLOYMENT = "https://socialspendingapp.com"

BASE = LOCALHOST

LOGIN_URL = f"{BASE}/login.php"
SIGNOUT_URL = f"{BASE}/signout.php"
SIGNUP_URL = f"{BASE}/signup.php"
FORGOT_PASSWORD_URL = f"{BASE}/forgot_password.php"

USER_ICON_UPLOAD_URL = f"{BASE}/user_icon_upload.php"
USER_INFO_URL = f"{BASE}/user_info.php"
USER_PROFILE_URL = f"{BASE}/user_profile.php"
SEARCH_USERS_URL = f"{BASE}/search_users.php"

INVALID_COOKIE = requests.cookies.cookiejar_from_dict({"session_id": "-1"})

NON_EXISTING_USER_LOGIN_PAYLOAD = {
    "user": "i_dont_exist",
    "password": "im_not_real",
    "remember": "false"
}

NON_EXISTING_EMAIL_LOGIN_PAYLOAD = {
    "user": "dbcooper@northwestorientairlines.com",
    "password": "password",
    "remember": "false"
}

EMPTY_LOGIN_PAYLOAD = {}

EMPTY_SIGNUP_PAYLOAD = {}

NEW_USER_SIGNUP_PAYLOAD = {
    "user": "new_user",
    "email": "new_user@example.com",
    "password": "password"
}

NEW_USER_LOGIN_PAYLOAD = {
    "user": "new_user",
    "password": "password",
    "remember": "false"
}

BJTN_SIGNUP_PAYLOAD = {
    "user": "level_five_yeti",
    "email": "BJTNoguera@socialspendingapp.com",
    "password": "password"
}

BJTN_EMAIL_LOGIN_PAYLOAD = {
    "user": "BJTNoguera@socialspendingapp.com",
    "password": "password",
    "remember": "false"
}

BJTN_LOGIN_PAYLOAD = {
    "user": "level_five_yeti",
    "password": "password",
    "remember": "false"
}

BJTN_TEST_LOGIN_PAYLOAD = {
    "user": "BJTN_test",
    "password": "password",
    "remember": "false",
}

BJTN_USER_INFO = {
    "user_id": 5,
    "username": "level_five_yeti",
    "message": "Success"
}

BJTN_USER_PROFILE = {
    "user_id": 5,
    "username": "level_five_yeti",
    "email": "BJTNoguera@socialspendingapp.com",
    "debt": 0,
    "message": "Success"
}

MATT_D_SEARCH_PROFILE = {
    "user_id": 1,
    "user": "Roasted715Jr",
}

MATT_F_SEARCH_PROFILE = {
    "user_id": 2,
    "user": "Soap_Ninja",
}

NICK_J_SEARCH_PROFILE = {
    "user_id": 3,
    "user": "Vanquisher",
}

RYDER_R_SEARCH_PROFILE = {
    "user_id": 4,
    "user": "Vasagle",
}

BJTN_SEARCH_PROFILE = {
    "user_id": 5,
    "user": "level_five_yeti",
}

BJTN_TEST_SEARCH_PROFILE = {
    "user_id": 8,
    "username": "BJTN_test,"
}

NON_EXISTING_USERNAME = {
    "user": "i_dont_exist"
}

NON_EXISTING_USER_ID = {
    "user_id": 69420
}

NON_EXISTING_USER_PROFILE = {
    "user_id": 69,
    "username": "ne"
}

def GET_VALID_COOKIE(user=None):
    """
    Returns session_id cookie from `user` account if specified, level_five_yeti account otherwise
    """
    if user:
        response = requests.post(LOGIN_URL, data=user)
    else:
        response = requests.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

    return response.cookies

