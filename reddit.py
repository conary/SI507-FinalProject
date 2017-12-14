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

#print('Joy:', emotion_emoji_dict['joy'])

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

def get_token():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": "conary", "password": "bot123"}
    headers = {"User-Agent": "conary/0.1"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    cred = json.loads(response.text)
    #print(cred)
    return cred['access_token']
    

def get_data(token, url):
    headers = {"Authorization": "bearer "+ token, "User-Agent": "conary/0.1"}
    #print(headers)
    response = requests.get(url, headers=headers)
    #print(response)
    data = json.loads(response.text)
    
    return data

def get_subreddit(token, url, query):
    post_data = {"exact": "false", "include_over_18": "true", "include_unadvertisable": "false", "query":query} 
    headers = {"Authorization": "bearer "+ token, "User-Agent": "osx:r/news.single.result:v0.1 (by /u/conary)"}
    response = requests.post(url, data=post_data, headers=headers)
    cred = json.loads(response.text)
    #print(cred)
    return cred


def get_posts(token, url):
    headers = {"Authorization": "bearer "+ token, "User-Agent": "osx:r/news.single.result:v0.1 (by /u/conary)"}
    response = requests.get(url, headers=headers)
    #print(response)
    datas = json.loads(response.text)
 
    print(datas)
    json_data = json.dumps(datas['data']['children'], indent=4, sort_keys=True)
    #print(json_data)
    data_all = datas['data']['children']
    #print(data_all)
    num_of_posts = 0
    while len(data_all) <= 100:
        time.sleep(2)
        last = data_all[-1]['data']['name']
        print(last)
        urls = 'https://www.reddit.com/r/news/.json?after=' + str(last)
        print(urls)
        req = requests.get(urls, headers=headers)
        data = json.loads(req.text)
        #data_all += data['data']['children']
        if num_of_posts == len(data_all):
            break
        else:
            num_of_posts = len(data_all)
    return data_all
    return json_data




#data_all += data.values()[1]['children']



token = get_token()
datas = get_data(token, 'https://oauth.reddit.com/api/v1/me/')
#print (datas)
subs = get_subreddit(token, 'https://oauth.reddit.com/api/search_reddit_names', 'trump')
#print (subs)
top_data = get_posts(token, 'https://oauth.reddit.com/r/news/.json')
#print(top_data)





#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, client_id=CLIENT_ID, scope=SCOPE)

#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, scope=SCOPE, client_id=CLIENT_ID)

#token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, auth=client_auth, grant_type='authorization_code')

