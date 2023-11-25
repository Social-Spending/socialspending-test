import requests

LOGIN_URL = "https://socialspendingapp.com/login.php"
SIGNOUT_URL = "https://socialspendingapp.com/signout.php"
SIGNUP_URL = "https://socialspendingapp.com/signup.php"
FORGOT_PASSWORD_URL = "https://socialspendingapp.com/forgot_password.php"

USER_ICON_UPLOAD_URL = "https://socialspendingapp.com/user_icon_upload.php"
USER_INFO_URL = "https://socialspendingapp.com/user_info.php"
USER_PROFILE_URL = "https://socialspendingapp.com/user_profile.php"
SEARCH_USERS_URL = "https://socialspendingapp.com/search_users.php"

CHECK = u"\u2705"
CROSS = u"\u274C"

INVALID_COOKIE = requests.cookies.cookiejar_from_dict({"session_id": "-1"})

NON_EXISTING_USER_LOGIN_PAYLOAD = {
    "user": "i_dont_exist",
    "password": "im_not_real"
}

NON_EXISTING_EMAIL_LOGIN_PAYLOAD = {
    "user": "dbcooper@northwestorientairlines.com",
    "password": "password"
}

EMPTY_LOGIN_PAYLOAD = {

}

EMPTY_SIGNUP_PAYLOAD = {

}

NEW_USER_SIGNUP_PAYLOAD = {
    "user": "new_user",
    "email": "new_user@example.com",
    "password": "password"
}

NEW_USER_LOGIN_PAYLOAD = {
    "user": "new_user",
    "password": "password"
}

BJTN_SIGNUP_PAYLOAD = {
    "user": "level_five_yeti",
    "email": "BJTNoguera@socialspendingapp.com",
    "password": "password"
}

BJTN_EMAIL_LOGIN_PAYLOAD = {
    "user": "BJTNoguera@socialspendingapp.com",
    "password": "password"
}

BJTN_LOGIN_PAYLOAD = {
    "user": "level_five_yeti",
    "password": "password"
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

def GET_VALID_COOKIES(user=None):
    """
    Returns session_id cookie from `user` account if specified, level_five_yeti account otherwise
    """
    if user:
        response = requests.post(LOGIN_URL, data=user)
    else:
        response = requests.post(LOGIN_URL, data=BJTN_LOGIN_PAYLOAD)

    return response.cookies
