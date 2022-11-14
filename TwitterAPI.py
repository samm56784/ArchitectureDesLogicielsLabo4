import requests

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACZnigEAAAAAKEX%2BtgiZRimdjsC6JctgZzmtj2Q%3DoSMCn4ImvCAIOBXBzd5dRUHZZgYRRSZDOzHnrVnTjhsFwhGPhk'


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
        try:
            response = requests.request('GET', url, headers=headers, params=params)
            if "errors" in response.json():
                print(response.json()['errors'][0]['message'])
                # print(response.json())
            print(response.json())
            return response.json()

        except:
            if url == '':
                response = "Invalid URL"
                return response
            print(requests.RequestException.request)
        #print(url)
        '''if "errors" in response.json():
            print(response.json()['errors'][0]['message'])
            #print(response.json())
        print(response.json())
        return response.json()'''



