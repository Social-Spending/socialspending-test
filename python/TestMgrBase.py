class TestMgrBase:
    # this should be overridden in sub classes
    # this function will be called to do all the steps to setup for the tests, and will be run before any tests
    def setup(self):
        self.tester_name = 'Base'
        # return false, this 'virtual' implementation should not be called
        return False
