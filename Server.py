from http.server import SimpleHTTPRequestHandler
from TwitterAPI import TwitterAPI
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http import HTTPStatus
import json

class Database:
    tweets = []
    nouveau_tweets = []

    def __init__(self):
        self.tweets = []

    def flush_tweets(self):
        del self.tweets[:]

    def save_tweets(self, new_tweets):
        self.tweets.extend(new_tweets)

    def load_tweets(self):
        return self.tweets
    def load_all_tweets(self) :
        return self.tweets


class Lab4HTTPRequestHandler(SimpleHTTPRequestHandler):
    db = Database()

    def do_GET(self):
        if self.path == '/':
            self.path = 'Search.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        if not (self.path.startswith('/queryTwitter') or self.path.startswith('/Afficher')):
            self.path = 'Display.html'
            tweets_to_display = '<div> <li>' + "erreur url...." + '</li> </div>'
            text_to_display = ''
            with open('Display.html', 'r') as file:
                text_to_display = f"{file.read()}".format(**locals())
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(text_to_display.encode('utf-8'))
            self.wfile.close()
            return


        if self.path.startswith('/queryTwitter'):
            data = ''
            query_components = parse_qs(urlparse(self.path).query)
            if 'query' in query_components:
                data = query_components['query'][0]
            try:
                headers = TwitterAPI.create_twitter_headers()
                url, params = TwitterAPI.create_twitter_url(data)
                json_response = TwitterAPI.query_twitter_api(url, headers, params)

            except json.decoder.JSONDecodeError as p:
                tweets_to_display = '<div> <li>' + "erreur headers" + '</li> </div>'
                text_to_display = ''
                with open('Display.html', 'r') as file:
                    text_to_display = f"{file.read()}".format(**locals())
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(text_to_display.encode('utf-8'))
                self.wfile.close()
                self.path = 'Display.html'
            except:
                tweets_to_display = '<div> <li>' + '</li> </div>'
                text_to_display = ''
                with open('Display.html', 'r') as file:
                    text_to_display = f"{file.read()}".format(**locals())

                self.wfile.write(text_to_display.encode('utf-8'))
                self.wfile.close()
                self.path = 'Display.html'
                return

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
                return

            else:
                try:
                    tweets = json_response['data']
                    nouveau_tweets = json_response['data']
                    self.db.save_tweets(tweets)
                    #self.db.save_new_tweets(nouveau_tweets)
                except json.decoder.JSONDecodeError as p:
                    tweets_to_display = '<div> <li>' + "erreur headers" + '</li> </div>'
                    text_to_display = ''
                    with open('Display.html', 'r') as file:
                        text_to_display = f"{file.read()}".format(**locals())
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    self.wfile.write(text_to_display.encode('utf-8'))
                    self.wfile.close()
                    self.path = 'Display.html'
                    return
                except:
                    print(json_response)
                    erreur=""
                    if "meta" in json_response:
                        erreur = "pas de resultat a la recherche"
                    else:
                        erreur = str(json_response)
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
                    return

                all_tweets = nouveau_tweets

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
                return

        elif self.path.startswith('/Afficher') :
            data = ' '
            headers = TwitterAPI.create_twitter_headers()
            url, params = TwitterAPI.create_twitter_url(data)
            json_response = TwitterAPI.query_twitter_api(url, headers, params)
            all_tweets = self.db.load_all_tweets()
            print(all_tweets)
            tweets_to_display = ''
            if len(all_tweets) == 0:
                tweets_to_display += '<div> <li>' + "Aucun Tweet a afficher..." + '</li> </div>'
            else:
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
        else :
            return

