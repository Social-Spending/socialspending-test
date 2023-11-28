# Social Spending Test

This repository contains test scripts to verify the functionality of the Social Spending website.

## Python Tests

### Prerequisites

* Python 3
* pip for Python 3
* [Requests](https://pypi.org/project/requests/)

To install the Requests Python module for Python 3, run `python3 -m pip install requests`.

### Running

Inside the `python` directory, run the `TestRunner.py` script:

```bash
cd ./python
python3 TestRunner.py
```

The above code with automatically discover all test managers and run each of them.

You may also run a specific test manager by passing the desired test manager name(s) as space-delimited command line argument(s). For example, the following code will run only the NotificationTestMgr:

```bash
python3 TestRunner.py NotificationsTestMgr
```

Another example, the following code will run only the NotificationTestMgr and GroupsTestMgr:

```bash
python3 TestRunner.py NotificationsTestMgr GroupsTestMgr
```

Note that the test runner searches for a class that inherits from `TestMgrBase` and has the same name as the provided command line argument(s). Although the file containing that class usually goes by the same name, you cannot search for a test manager by the file it is in.

#### Debugging in VS Code

If you are running VS Code, a `launch.json` file is included that is already setup to run the `TestRunner.py` file in debugging mode. Simply click the 'Run & Debug' tab on the left sidebar and click Run.

If you would like to debug one specific test manager, add a string with the name(s) of the test manger(s) to the `"args"` array under the `"TestRunner (python)"` configuration in `launch.json`. For example, setting it to the following will run only the NotificationTestMgr:

```json
"args": ["NotificationsTestMgr"]
```

Another example, the following code will run only the NotificationTestMgr and GroupsTestMgr:

```json
"args": ["NotificationsTestMgr", "GroupsTestMgr"]
```

### Developing a Test Manager

The "test manager" is a class that inherits from `TestMgrBase`, and contains 1) a method to setup for the test and 2) one or more test methods to run.

#### Step 1: Create Files

Create a new folder with the name of the component you will be testing. Inside this folder, create an empty file name `__init__.py`; this tells the Python interpreter to treat this folder as a module. Also inside this folder, create the file that will contain your test manager. Any name will work, but by convention, the name of this file should be `ComponentTestMgr.py`, replacing 'Component' in your case.

Any supporting files, such as txt, csv, or other python files used by your test manager should also go in this folder.

The (abbreviated) directory structure should similar like this, again replacing 'Component' in your case:
```
├─ python
│  ├─ Component
│  │  ├── ComponentTestMgr.py
│  │  ├── __init__.py
│  │  ├── SupportingFile.csv
│  ├─ TestMgrBase.py
│  ├─ TestRunner.py
│  ├─ __init__.py
```

#### Step 2: Creating the Test Manager Class

_Note: Everywhere it is mentioned, replace 'Component' with the component this class tests, ie. 'Groups', 'Login'_

Inside your `ComponentTestMgr.py` file created in step 1, copy the following code (it will be explained later):

```python
from TestMgrBase import TestMgrBase
import requests
import json

class ComponentTestMgr(TestMgrBase):
    # this function will be called to do all the steps to setup for the tests, ...
    # and will be run before any tests
    def setup(self):
        self.tester_name = 'ComponentTestMgr'
        return True

    def test_nominal(self):
        print('This always returns False')
        return False
```

Note that the `requests` and `json` imports are not used in the example code, but are useful modules for dealing with HTTP requests to backend elements.

Any class inheriting from `TestMgrBase` will be ran by `TestRunner.py`, but by convention your class should be of the form `ComponentTestMgr`. Note that, because your class inherits `TestMgrBase`, it has access to all helper functions in `TestMgrBase`.

The `setup` method overrides the method from `TestMgrBase`. It should perform any actions needed by your test cases, such as logging in. `setup` must return `True` if the setup was successful, otherwise return `False`. If `setup` returns `False` or raises and exception, no test methods will be run.

Your test manager may have any number of test methods. The name of the test is described by the method name, and test methods must start with the word 'test'. By convention, test methods start with `test_`. Test methods must return a boolean that is `True` if the test passed and `False` if the test failed.

Exceptions raised in `setup` or in test methods will be caught and printed, and it will be treated as if that function returned `False`.

When run, the `setup` method and test methods will be enclosed by headers before and after the method was run, so any print statements inside these methods can be reliably traced back to the method that printed them. If a test fails, your test method should should have a print statement detailing what caused the failure before returning from the method.

Running the above example test manager looks like this:

```
-------------Running ComponentTestMgr.setup-------------
-------------ComponentTestMgr.setup SUCCESS-------------

-------------Running Test ComponentTestMgr.test_nominal-------------
This always returns False
-------------FAIL Test ComponentTestMgr.test_nominal-------------

-------------Results Summary ComponentTestMgr-------------
1 Ran, 0 Passing, 1 Failing
-------------Overall FAIL-------------
```

Note that in the above output, the name of the test method is printed. Give your test methods descriptive names to give this output good meaning.

#### Parting Remarks

Note that, because your class inherits `TestMgrBase`, it has access to all helper functions in `TestMgrBase`. Any functions you create that could have utility across other test managers should be implemented in the base class.

Remember, magic values used in lots of places, like a URL address or credentials, should be defined in global constants.

## Bash Test

### Prerequisites

* curl
* Python 3

These scripts have only been tested on a Linux system.

### Running

Simply run the shell script. These tests require manual inspection of the output.
