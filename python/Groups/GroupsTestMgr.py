from TestMgrBase import TestMgrBase
import requests
import json

SERVER = "http://localhost"
GROUPS_ENDPOINT = SERVER + "/groups.php"
GROUPS_ICON_UPLOAD_ENDPOINT = SERVER + "/group_icon_upload.php"
USERNAME = "Soap_Ninja"
PASSWORD = "password"

class GroupsTestMgr(TestMgrBase):
    # this function will be called to do all the steps to setup for the tests, and will be run before any tests
    def setup(self):
        self.tester_name = 'GroupsTestMgr'
        # create a session for all those delicious cookies
        self.cookieJar = self.login(USERNAME, PASSWORD)
        return True

    def getGroups(self):
        response = self.session.get(GROUPS_ENDPOINT, cookies=self.cookieJar)
        if response.status_code != 200:
            raise Exception("Failed to get groups info, status code " + str(response.status_code))
        # response.json will raise exception if it cannot be parsed
        return response.json()

    def getGroupInfo(self, groupID):
        response = self.session.get(GROUPS_ENDPOINT + '?groupID=' + str(groupID), cookies=self.cookieJar)
        if response.status_code != 200:
            raise Exception("Failed to get specific group info, status code " + str(response.status_code))
        # response.json will raise exception if it cannot be parsed
        return response.json()

    def test_getGroups(self):
        actualJSON = self.getGroups()
        # expected JSON is based on the example data defined the database.sql
        expectedJSON = \
            {
                "message": "Success",
                "groups":
                [
                    {
                        "group_id": 1,
                        "group_name": "CMSC447 Bros",
                        "icon_path": None,
                        "debt": 1000,
                        "transactions":
                        [
                            {
                                "transaction_id": 1,
                                "name": "Halal Shack",
                                "date": "2023-09-29",
                                "group_id": 1,
                                "user_debt": 500,
                                "is_approved": 1
                            },
                            {
                                "transaction_id": 3,
                                "name": "Coffee Run",
                                "date": "2023-10-25",
                                "group_id": 1,
                                "user_debt": 500,
                                "is_approved": 1
                            }
                        ],
                        "members":
                        [
                            {
                                "user_id": 1,
                                "username": "Roasted715Jr",
                                "icon_path": None,
                                "debt": -501
                            },
                            {
                                "user_id": 3,
                                "username": "Vanquisher",
                                "icon_path": None,
                                "debt": -799
                            },
                            {
                                "user_id": 4,
                                "username": "Vasagle",
                                "icon_path": None,
                                "debt": 300
                            },
                            {
                                "user_id": 5,
                                "username": "level_five_yeti",
                                "icon_path": None,
                                "debt": 0
                            }
                        ],
                        "pending_invites":[]
                    },
                    {
                        "group_id": 2,
                        "group_name": "Matts",
                        "icon_path": None,
                        "debt": 500,
                        "transactions":
                        [
                            {
                                "transaction_id": 2,
                                "name": "Gas Money",
                                "date": "2023-10-30",
                                "group_id": 2,
                                "user_debt": -500,
                                "is_approved": 0
                            }
                        ],
                        "members":
                        [
                            {
                                "user_id": 1,
                                "username": "Roasted715Jr",
                                "icon_path": None,
                                "debt": -500
                            }
                        ],
                        "pending_invites":[]
                    }
                ]
            }
        return self.matchingJSON(expectedJSON, actualJSON)


    def test_getGroupsBrief(self):
        response = self.session.get(GROUPS_ENDPOINT + '?brief=true', cookies=self.cookieJar)
        if response.status_code != 200:
            print("Failed to get group info brief, status code " + str(response.status_code))
            return False
        # response.json will raise exception if it cannot be parsed
        actualJSON = response.json()
        # expected JSON is based on the example data defined the database.sql
        expectedJSON = \
            {
                "message": "Success",
                "groups":
                [
                    {
                        "group_id": 1,
                        "group_name": "CMSC447 Bros",
                        "icon_path": None,
                        "debt": "1000"
                    },
                    {
                        "group_id": 2,
                        "group_name": "Matts",
                        "icon_path": None,
                        "debt":"500"
                    }
                ]
            }
        if not self.matchingJSON(expectedJSON, actualJSON):
            return False
        # also check that "members", "transactions", and "pending_invites" are NOT set
        for group in actualJSON['groups']:
            for badNode in ["members", "transactions", "pending_invites"]:
                if badNode in group:
                    return False
        return True

    def test_getGroupsNoDebts(self):
        response = self.session.get(GROUPS_ENDPOINT + '?nodebts=true', cookies=self.cookieJar)
        if response.status_code != 200:
            print("Failed to get group info brief, status code " + str(response.status_code))
            return False
        # response.json will raise exception if it cannot be parsed
        actualJSON = response.json()
        # expected JSON is based on the example data defined the database.sql
        expectedJSON = \
            {
                "message": "Success",
                "groups":
                [
                    {
                        "group_id": 1,
                        "group_name": "CMSC447 Bros",
                        "icon_path": None,
                        "members":
                        [
                            {
                                "user_id": 1,
                                "username": "Roasted715Jr",
                                "icon_path": None,
                            },
                            {
                                "user_id": 3,
                                "username": "Vanquisher",
                                "icon_path": None,
                            },
                            {
                                "user_id": 4,
                                "username": "Vasagle",
                                "icon_path": None,
                            },
                            {
                                "user_id": 5,
                                "username": "level_five_yeti",
                                "icon_path": None,
                            }
                        ],
                        "pending_invites":[]
                    },
                    {
                        "group_id": 2,
                        "group_name": "Matts",
                        "icon_path": None,
                        "members":
                        [
                            {
                                "user_id": 1,
                                "username": "Roasted715Jr",
                                "icon_path": None,
                            }
                        ],
                        "pending_invites":[]
                    }
                ]
            }
        if not self.matchingJSON(expectedJSON, actualJSON):
            return False
        # also check that "transactions", and "debt" are NOT set
        for group in actualJSON['groups']:
            if "transactions" in group:
                return False
            if 'debt' in group:
                return False
            for member in group['members']:
                if 'debt' in member:
                    return False
        return True

    def test_getSpecificGroupInfo(self):
        actualJSON = self.getGroupInfo(100)
        return False

    def test_stub2(self):
        return True
