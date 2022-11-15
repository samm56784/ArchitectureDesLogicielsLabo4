import unittest
from Server import Database
from TwitterAPI import TwitterAPI

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db = None

    def test_can_load_tweets(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertIsNotNone(json_response['data'])

    def test_delete_tweet_db(self):
        tweet = {
            "username": "sdumas",
            "tweet": "Je fais un tweet!"
        }
        self.db.tweets = [tweet]
        saved_tweet = self.db.load_tweets()
        saved_tweet = self.db.flush_tweets()
        self.assertIsNone(saved_tweet)

    def test_can_save_tweets_in_database(self):
        tweet = {
            "username": "sdumas",
            "tweet": "Bonjour!"
        }
        self.db.tweets = [tweet]
        saved_tweets = self.db.load_tweets()
        self.assertEqual(saved_tweets[0], tweet)

    def test_pas_de_header(self):
        headers = ''
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertEqual(str(json_response), "Expecting value: line 1 column 1 (char 0)")

    def test_header_invalide(self):
        headers = 'cmmkmkmkvmsdkmvksmvlkmslkvmsklvmslkvsm'
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(str(json_response), "Expecting value: line 1 column 1 (char 0)")
    def test_url_non_valide(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        url = 'bjkfbskdfsjkbfd'
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
       # print(json_response)
        self.assertIn("Invalid URL", str(json_response) )
    def test_query_a(self): #pour x raison la lettre a seule crée une erreur, je fais donc un test pour voir si le tout est géré
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('a')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['errors'][0]['message'],
                         "There were errors processing your request: Rules must contain at least one positive, non-stopword clause (at position 1)")
    def test_aucun_resultat(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('ggUYDGUYAgduyasgydgsgfuygafkufgkjhfgsajhkfgajkhsfgjakhsdgfajhksfgjahskdgfasjkhdfgajhkfg')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response, {'meta': {'result_count': 0}})
    def test_query_vide(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['errors'][0]['message'], "Invalid 'query':''. 'query' must be a non-empty string")


class TestServer(unittest.TestCase):
    pass


class TestTwitterAPI(unittest.TestCase):
    pass
