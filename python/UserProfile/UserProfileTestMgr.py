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

class UserProfileTestMgr(TestMgrBase):
    def setup(self):
        self.tester_name = "UserProfileTestMgr"




