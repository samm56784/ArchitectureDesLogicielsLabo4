import unittest
from Server import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db = None

    def test_can_load_tweets(self):
        testvalue = False
        message = "not false"

        self.assertFalse(testvalue, message)


class TestServer(unittest.TestCase):
    pass


class TestTwitterAPI(unittest.TestCase):
    pass
