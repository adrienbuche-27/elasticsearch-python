import urllib.request, urllib.parse, urllib.error
import requests
import oauth
import hidden

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

def augment(url, parameters):
    secrets = hidden.oauth()
    consumer = oauth.OAuthConsumer(secrets['consumer_key'],
                                   secrets['consumer_secret'])
    token = oauth.OAuthToken(secrets['token_key'], secrets['token_secret'])

    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                    token=token, http_method='GET', http_url=url,
                    parameters=parameters)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                               consumer, token)
    return oauth_request.to_url()

def augment_search(url, parameters):
    secrets = hidden.oauth()
    consumer = oauth.OAuthConsumer(secrets['consumer_key'],
                                   secrets['consumer_secret'])
    
    r = requests.post('https://api.twitter.com/oauth2/token',
                  auth=(consumer.key, consumer.secret),
                  headers={'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},
                  data='grant_type=client_credentials').json()
    
    if r['token_type'] == 'bearer':
        bearer = r['access_token']
        return requests.get(url, headers={'Authorization': 'Bearer ' + bearer}, params=parameters)
    else:
        bearer = None
        return None
    
def test_me():
    print('* Calling Twitter...')
    url = augment('https://api.twitter.com/1.1/statuses/user_timeline.json',
                  {'screen_name': 'drchuck', 'count': '2'})
    print(url)
    connection = urllib.request.urlopen(url)
    data = connection.read()
    print(data)
    headers = dict(connection.getheaders())
    print(headers)
