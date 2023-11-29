from TestMgrBase import TestMgrBase

class GroupsTestMgr(TestMgrBase):
    # this should be overridden in sub classes
    # this function will be called to do all the steps to setup for the tests, and will be run before any tests
    def setup(self):
        self.tester_name = 'GroupsTestMgr'
        return False

    def test_stub(self):
        return False

    def test_stub2(self):
        return True
