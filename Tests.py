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

    def test_pas_bearer_token(self):
        headers = TwitterAPI.create_twitter_headers('')
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(str(json_response), "Expecting value: line 1 column 1 (char 0)")

    def test_bearer_token_invalide(self):
        headers = TwitterAPI.create_twitter_headers('khiusdhuvhsiushuhvsudviusdhvd')
        url, params = TwitterAPI.create_twitter_url(
            'allo')
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertEqual(str(json_response), "Expecting value: line 1 column 1 (char 0)")

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

    def test_aucun_params(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('query parameter can not be empty', str(json_response))

    def test_expansions_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 10,
            'expansions': 'bdkjsdbkjsbckcjbskjcsdkjbkjsbkjscbdk',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('expansions', str(json_response))
        self.assertIn('is not one of', str(json_response))

    def test_tweetfield_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'ouhuhoisdhcoihscohdsoicsdhcoishcoisdhcsdoihds',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('tweet.field', str(json_response))
        self.assertIn('is not one of', str(json_response))

    def test_userfield_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'woihwiohiowehciowehwheiohcoiwhciowecoih',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('user.field', str(json_response))
        self.assertIn('is not one of', str(json_response))

    def test_placefield_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'guiasguasuidgiausgdiuasduiadgaiud',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('place.field', str(json_response))
        self.assertIn('is not one of', str(json_response))

    def test_maxresults_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': '',
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('max_results', str(json_response))
        self.assertIn('is not a valid Int', str(json_response))
    def test_maxresultszero_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 0,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('max_results', str(json_response))
        self.assertIn('is not between 10 and 100', str(json_response))

    def test_nexttoken_params_invalides(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url('allo')
        params.clear()
        params = {
            'query': 'allo',
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token':' hjkchvjhjchvsdjhcsdcjhvscjhvjhvjhsdvcjhsdvjcshcvsjhcvsdjscvsjvchs'
        }
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)
        self.assertIn('next_token', str(json_response))
        self.assertIn('is not a valid token', str(json_response))




class TestServer(unittest.TestCase):
    pass


class TestTwitterAPI(unittest.TestCase):
    pass
