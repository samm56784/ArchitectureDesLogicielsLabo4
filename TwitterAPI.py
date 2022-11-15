import requests
import json

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACZnigEAAAAAMr%2BgKhxvcosY%2Fip0F%2BJYiaS7wc8%3DrKVUpzuW33iTxgazWhhMBzbzYO75BvIQ1cPrFjiEWPquRKibux'


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
            if type(headers) != dict:
                header = json.loads(headers)
            else:
                header = headers
            #header = json.loads(headers)
            response = requests.request('GET', url, headers=header, params=params)
            print(response)
            if "errors" in response.json():
                print(response.json()['errors'][0]['message'])
                # print(response.json())
            elif "title" in response.json():
                print(response.json()['type'])
            print(response.json())
            return response.json()

        except requests.exceptions.RequestException as e:
            response = e
            print(e)
            return response
        except requests.exceptions.InvalidHeader as a:
            response = a
            print(a)
            return response
        except requests.exceptions.BaseHTTPError as h:
            response = h
            print(h)
            return response
        except requests.HTTPError as g:
            response = g
            print(g)
            return response
        except requests.RequestException as t:
            print(t)
            return t
        except requests.exceptions.InvalidJSONError as j:
            print(j)
            return
        except requests.exceptions.MissingSchema as s:
            print(s)
            return s
        except requests.exceptions.JSONDecodeError as d:
            print(d)
            return d
        except requests.exceptions.InvalidSchema as v:
            print(v)
            return v
        except requests.exceptions.RequestsWarning as w:
            print(w)
            return w
        except json.decoder.JSONDecodeError as p:
            print(p)
            return p
            #if url == '':
                #print(requests.RequestException)
                #response = "URL vide"
                #return response
            #print(requests.RequestException.request)
        #print(url)
        '''if "errors" in response.json():
            print(response.json()['errors'][0]['message'])
            #print(response.json())
        print(response.json())
        return response.json()'''



