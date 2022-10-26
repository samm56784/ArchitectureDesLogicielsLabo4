import requests

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACZnigEAAAAAOBEkkp0cQ1oc5LFfwngqLnWQDl4%3D4Uqkn5LTHisSxXbYdrRPgos2TG5h7l1IxjM2q62G2sIzlrRAoy'


class TwitterAPI:
    @staticmethod
    def create_twitter_headers():
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        return headers

    @staticmethod
    def create_twitter_url(keyword, max_results=10):
        search_url = 'https://api.twitter.com/2/tweets/search/recent'

        query_params = {
            'query': keyword,
            'max_results': max_results,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }
        return search_url, query_params

    @staticmethod
    def query_twitter_api(url, headers, params):
        response = requests.request('GET', url, headers=headers, params=params)
        return response.json()



