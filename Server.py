from http.server import SimpleHTTPRequestHandler
from TwitterAPI import TwitterAPI
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http import HTTPStatus


class Database:
    tweets = []

    def __init__(self):
        self.tweets = []

    def flush_tweets(self):
        del self.tweets[:]

    def save_tweets(self, new_tweets):
        self.tweets.extend(new_tweets)

    def load_tweets(self):
        return self.tweets
    def load_new_tweets(self) :
        nombreEntrées = len(self.tweets)
        newTweets=[]
        newTweets= self.tweets[nombreEntrées-10:nombreEntrées]
        return newTweets
    def load_all_tweets(self) :
        return self.tweets


class Lab4HTTPRequestHandler(SimpleHTTPRequestHandler):
    db = Database()

    def do_GET(self):
        if self.path == '/':
            self.path = 'Search.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        if not (self.path.startswith('/queryTwitter') or self.path.startswith('/Afficher')) :
            self.path = 'Search.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        if self.path.startswith('/queryTwitter'):
            data = ''

            query_components = parse_qs(urlparse(self.path).query)
            if 'query' in query_components:
                data = query_components['query'][0]

            headers = TwitterAPI.create_twitter_headers()
            url, params = TwitterAPI.create_twitter_url(data)
            try:
                json_response = TwitterAPI.query_twitter_api(url, headers, params)
            except:
                print(json_response)
                tweets_to_display = '<div> <li>' + '</li> </div>'
                text_to_display = ''
                with open('Display.html', 'r') as file:
                    text_to_display = f"{file.read()}".format(**locals())
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(text_to_display.encode('utf-8'))
                self.wfile.close()
                self.path = 'Display.html'

            #print(json_response)
            #tweets = json_response['data']
            if "errors" in json_response:
                erreur = json_response['errors'][0]['message']
                tweets_to_display = '<div> <li>' + erreur + '</li> </div>'

                text_to_display = ''
                with open('Display.html', 'r') as file:
                    text_to_display = f"{file.read()}".format(**locals())

                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(text_to_display.encode('utf-8'))
                self.wfile.close()

                self.path = 'Display.html'

            else:
                try:
                    tweets = json_response['data']
                except:
                    erreur=""
                    if "meta" in json_response:
                        erreur = "pas de resultat a la recherche"
                    tweets_to_display = '<div> <li>' + erreur + '</li> </div>'
                    text_to_display = ''
                    with open('Display.html', 'r') as file:
                        text_to_display = f"{file.read()}".format(**locals())
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    self.wfile.write(text_to_display.encode('utf-8'))
                    self.wfile.close()
                    self.path = 'Display.html'

                self.db.save_tweets(tweets)

                # Assume that right here, we load the tweets from a SQL database

                all_tweets = self.db.load_new_tweets()

                tweets_to_display = ''
                for tweet in all_tweets:
                    tweets_to_display += '<div> <li>' + tweet['text'] + '</li> </div>'

                text_to_display = ''
                with open('Display.html', 'r') as file:
                    text_to_display = f"{file.read()}".format(**locals())

                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(text_to_display.encode('utf-8'))
                self.wfile.close()

                self.path = 'Display.html'


            # Assume that right here, we save the tweets into a SQL databases
           # self.db.flush_tweets()
        elif self.path.startswith('/Afficher') :
            data = ' '

           # query_components = parse_qs(urlparse(self.path).query)
            #if 'query' in query_components:
               # data = query_components['query'][0]

            headers = TwitterAPI.create_twitter_headers()
            url, params = TwitterAPI.create_twitter_url(data)
            json_response = TwitterAPI.query_twitter_api(url, headers, params)
            #tweets = json_response['data']
            all_tweets = self.db.load_all_tweets()
            print(all_tweets)
            tweets_to_display = ''
            if len(all_tweets) == 0:
                tweets_to_display += '<div> <li>' + "Aucun Tweet a afficher..." + '</li> </div>'
            else:
                for tweet in all_tweets:
                    tweets_to_display += '<div> <li>' + tweet['text'] + '</li> </div>'

            text_to_display = ''
            with open('Allo.html', 'r') as file:
                text_to_display = f"{file.read()}".format(**locals())

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(text_to_display.encode('utf-8'))
            self.wfile.close()

            self.path = 'Allo.html'
        else :
            return

