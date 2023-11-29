import os
from TestMgrBase import TestMgrBase
import inspect

DELIMITER = '-------------'

class TestMgrRef:
    def __init__(self, moduleName):
        self.moduleName = moduleName

    # attempt to import classes from the module where the class inherits from TestMgrBase
    # returns true if a class inheriting from TestMgrBase was found
    def importCls(self):
        # import the module by the string name
        # module search path will contain the path that this file (TestRunner.py) is in, which is good
        # split the module name into the hierarchy, delimited by dot '.'
        components = self.moduleName.split('.')
        # import the top level module
        mod = __import__(self.moduleName)
        # go down the tree until we've found the module we're looking for
        for comp in components[1:]:
            mod = getattr(mod, comp)
        # get all classes from that module
        # inspect.getmembers returns (name, value) pairs
        classes = inspect.getmembers(mod, inspect.isclass)
        # store only the classes that inherit from TestMgrBase
        classes = [(name,cls) for name,cls in classes if issubclass(cls, TestMgrBase) and cls != TestMgrBase]

        # take only the first class
        if len(classes) == 1:
            # store the class name and the class
            self.name, self.cls = classes[0]
            return True
        # display error if there were more than one class ?
        elif len(classes) > 0:
            print('Module '+self.moduleName+' contains multiple classes inheriting from TestMgrBase')
        # no class was found inheriting from TestMgrBase
        return False

    # run the 'setup' method for all TestMgr classes
    def runSetup(self):
        print(DELIMITER + 'Running ' + self.name + '.setup' + DELIMITER)
        result = False
        try:
            # create an instance of the class and run setup method
            self.instance = self.cls()
            result = self.instance.setup()
        except Exception as err:
            print(err)
        print(DELIMITER + self.name + '.setup ' + ('SUCCESS' if result else 'FAILURE') + DELIMITER + '\n')
        return result


    # run all methods starting with 'test'
    def runTests(self):
        # initialize test success count and total count
        self.tests = 0
        self.successes = 0
        # get methods starting with 'test'
        testMethods = inspect.getmembers(self.instance, inspect.ismethod)
        testMethods = [(name, meth) for name,meth in testMethods if name.startswith('test')]
        # run all methods
        for methName, meth in testMethods:
            print(DELIMITER + 'Running Test ' + self.name + '.' + methName + DELIMITER)
            result = False
            try:
                result = meth()
            except Exception as err:
                print(err)
            print(DELIMITER + ('PASS:' if result else 'FAIL"') + ' Test ' + self.name + '.' + methName + DELIMITER + '\n')
            self.tests += 1
            self.successes += 1 if result else 0
        # return if all tests passed
        return self.tests == self.successes

    def reportTests(self):
            print(DELIMITER + 'Results Summary ' + self.name + DELIMITER)
            print(str(self.tests) + ' Ran, ' + str(self.successes) + ' Passing, ' + str(self.tests - self.successes) + ' Failing')
            print(DELIMITER + 'Overall ' + ('PASS' if self.tests == self.successes else 'FAIL') + DELIMITER + '\n')


class TestRunner:
    def __init__(self):
        # search current dir for all test classes
        # array of TestMgrReg test
        self.testMgrRefList = []

        # start looking at files in the root dir
        dirList = os.listdir('./')
        for node in dirList:
            # check that file is a .py file
            if os.path.isfile(node) and node[-3:] == '.py' and node != '__init__.py' and node != 'TestRunner.py':
               # the module name is the filename without the '.py'
               self.testMgrRefList.append(TestMgrRef(node[0:-3]))

            if os.path.isdir(node):
                # look in 1 level of folder
                dirList2 = os.listdir('./'+ node)
                # this folder is only a 'module' to the interpreter if it contains __init__.py
                if '__init__.py' in dirList2:
                    for node2 in dirList2:
                        # check that file is a .py file
                        if os.path.isfile(os.path.join(node,node2)) and node2[-3:] == '.py' and node2 != '__init__.py':
                            # module name is the <dir name>.<python script without the .py>
                            self.testMgrRefList.append(TestMgrRef(node + '.' + node2[0:-3]))

    def importClasses(self):
        # import classes from each file
        # only keep references containing a class derived from TestMgrBase
        self.testMgrRefList = [ref for ref in self.testMgrRefList if ref.importCls()]

    def runClasses(self):
        for ref in self.testMgrRefList:
            if ref.runSetup():
                ref.runTests()
                ref.reportTests()


if __name__ == '__main__':
    testRunner = TestRunner()
    testRunner.importClasses()
    testRunner.runClasses()
