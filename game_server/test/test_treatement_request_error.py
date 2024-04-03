import unittest

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import treatement.treatement_request_error as tro


class TestTreatementError(unittest.TestCase):
    def test_login(self):
        # en supposant qu'un joueur test0 n'est pas dans la BDD
        self.assertFalse(tro.check_login("test0"))
        # en supposant qu'un joueur test1 est dans la BDD
        self.assertTrue(tro.check_login("test1"))

if __name__ == '__main__':
    unittest.main()
