import unittest


def suite():
    suite = unittest.TestSuite()
    for test in unittest.TestLoader().discover('.'):
        suite.addTest(test)
    return suite
