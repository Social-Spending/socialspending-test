import requests
from itertools import permutations

SERVER = "http://localhost"
LOGIN_ENDPOINT = SERVER + "/login.php"

class TestMgrBase:
    # this should be overridden in sub classes
    # this function will be called to do all the steps to setup for the tests, and will be run before any tests
    def setup(self):
        self.tester_name = 'Base'
        # return false, this 'virtual' implementation should not be called
        return False

    # returns a RequestsCookieJar object with a session_id cookie,...
    #  authenticated with the given username and password
    def login(self, username, password):
        response = requests.post(LOGIN_ENDPOINT, data={"user": username, "password": password, "remember": "false"})
        if (response.status_code != 200):
            raise Exception("Failed to log in, status code "+str(response.status_code))
        cookieJar = response.cookies
        if 'session_id' not in cookieJar.keys:
            raise Exception("Failed to log in, session_id cookie not set")

        return cookieJar

    # returns true if the actual object has the same keys in the expected object, ...
    # and those keys have have same values
    def matchingJSON(self, expected, actual):
        # if the passed object is a dictionary
        if isinstance(expected, dict):
            for expectKey, expectValue in expected:
                if expectKey not in actual:
                    return False
                    #raise Exception("key \'" + expectKey + "\' not in actual JSON")
                if not self.matchingJSON(expectValue, actual[expectKey]):
                    return False

        # the passed object is otherwise a list
        elif hasattr(expected, '__iter__'):
            # expected and actual must be the same length
            if (len(expected) != len(actual)):
                #raise Exception("Arrays do not have matching lengths")
                return False
            # some number of permutations must exists
            # If expected=[A, B] and actual = [C, D]...
            # combinations=[ [(A,C), (B, D)], [(B,C), (A,D)] ]
            combinations = []
            for object in permutations(expected, len(actual)):
                combinations.append(zip(object, actual))
            for combination in combinations:
                numMatches = 0
                for expectedObj, actualObj in combination:
                    if self.matchingJSON(expectedObj, actualObj):
                        numMatches += 1
                if numMatches == len(combination) - 1:
                    return True
            # none of the combinations return True
            return False

        # comparing actual values, these are primitive types
        return expected == actual
        # elif (expected != actual):
            # raise Exception("Expected value \'" + expected + \
            #                 "\' does not actual value \'" + actual)
        # return True
