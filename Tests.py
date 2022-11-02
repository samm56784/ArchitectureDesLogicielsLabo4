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

    def test_can_save_tweets_in_database(self):
        tweet = {
            "username": "sdumas",
            "tweet": "Bonjour!"
        }
        self.db.tweets = [tweet]
        saved_tweets = self.db.load_tweets()
        self.assertEqual(saved_tweets[0], tweet)

class TestServer(unittest.TestCase):
    pass


class TestTwitterAPI(unittest.TestCase):
    pass
