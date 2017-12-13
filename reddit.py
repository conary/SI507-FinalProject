# -*- coding: utf-8 -*-
import requests
import requests_oauthlib
import requests.auth
import webbrowser
import json
import secret_data
import random
import string
import time

emotion_emoji_dict = {
    'anger': "😡",
    'joy': "😃",
    'fear': "",
    'sadness': "",
    'surprise': ""
}

print('Joy:', emotion_emoji_dict['joy'])



# CONSTANTS

CLIENT_ID = secret_data.client_id 
CLIENT_SECRET = secret_data.client_secret #'get this from spotify or create a secret data file, see spotify_data.py

AUTHORIZATION_URL = 'https://www.reddit.com/api/v1/authorize'
# NOTE: you need to specify this same REDIRECT_URI in the Spotify API console of your application!
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth' # This is a URL we have specifically set up at UMSI to handle student requests, basically -- it is an "OAuth2 workaround". You could use any URL -- but it would be a bit rude to, because that's still a hit on someone's URL! In general, you'd use your own -- on your own server.
TOKEN_URL = 'https://ssl.reddit.com/api/v1/access_token'
#SCOPE = ['identity','flair','read']
SCOPE = ['identity']
TYPE = ['code']






def create_state_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

STATE = create_state_string(10)

# Set up sessions and so on to get data via OAuth2 protocol...

#oauth2inst = requests_oauthlib.OAuth2Session(client_id=CLIENT_ID, response_type=TYPE, state=STATE, redirect_uri=REDIRECT_URI, scope=SCOPE) # Create an instance of an OAuth2Session
#oauth2inst = requests_oauthlib.OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE) # Create an instance of an OAuth2Session

#authorization_url, state = oauth2inst.authorization_url(AUTHORIZATION_URL) 
#print(authorization_url)




 

#webbrowser.open(authorization_url) 
#authorization_response = input('Authenticate and then enter the full callback URL: ').strip() # Need to get the full URL in order to parse the response






def get_token():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": "conary", "password": "bot123"}
    headers = {"User-Agent": "conary/0.1"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    cred = json.loads(response.text)
    print(cred)
    return cred['access_token']
    

def get_data(token, url):
    headers = {"Authorization": "bearer 3E_eJvL2kwpvyKcSGuC8tVkKpo4", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
 
    return data


token = get_token()
datas = get_data(token, 'https://oauth.reddit.com/api/v1/me/prefs')
print (datas)





#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, client_id=CLIENT_ID, scope=SCOPE)

#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, scope=SCOPE, client_id=CLIENT_ID)

#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, grant_type='authorization_code')





# state: unique string for your own use
# scope: 'identity'
# client_id: The client_id assigned by reddit
# redirect_uri: the redirect_uri you assigned.
# code: the code received in step 4.
# grant_type: 'authorization_code




#print(token)
## On a web server, this would happen on your server, but we have to pull the token out so we can use it for a request inside a script we're running on a personal computer (with connection to internet)
## Anytime we want to get new data we have to do this -- so a caching system would have to take this into account any time the data expired.
## And for that -- we'd want to think about the API rate limits, primarily!

# Now we can just use the get method on the oauth2session instance from here on out to make requests to spotify endpoints. Token will work for any endpoint, as long as it's still valid. (How long it is will depend from API to API)
#r = oauth2inst.get('https://www.reddit.com/api/v1/me')
#response_diction = json.loads(r.text)
#print(json.dumps(response_diction, indent=2)) # See the response printed neatly -- uncomment

###########
## Of course, this code does not have a caching setup,
## NOR does it have a set of useful functions --
## This is simply showing the process of managing an OAuth2Session.

## HOWEVER, the process here is actually simpler than ONE (not all) of the ways to address dealing with OAuth1 Protocol, though in the background, it is more in depth.

## NOTE: If not using oauth2, and you just need to extract a code from the URL, you can try something sort of like this... it is pretty ugly parsing of a URL, but it might get the job done:
# parts = authorization_response.split('?')
# query_parts = parts[1].split('&')
# code = ""
# for part in query_parts:
#     if part[:len("access_token")] == "access_token=":
#         code = part[5:]
# print(code) # or whatever you need to use it for
