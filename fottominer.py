#!/usr/bin/env python

import json

from twython import Twython

def load_oauth_keys(file_name='auth.json'):
    auth_file = file(file_name)
    auth_json = auth_file.read()
    auth_file.close()

    auth_dict = json.loads(auth_json)
    return auth_dict

def get_access_token(auth_dict):
    twitter = Twython(auth_dict['CONSUMER_KEY'], auth_dict['CONSUMER_SECRET'], oauth_version=2)
    return twitter.obtain_access_token()

def main():
    print 'Loading keys...'
    auth_dict = load_oauth_keys()

    print 'Acquiring access token...'
    access_token = get_access_token(auth_dict)

    print 'Authenticating with access token...'
    twitter = Twython(auth_dict['CONSUMER_KEY'], access_token=access_token)

    print 'Searching...'
    twitter.search(q='#tulongthursday')
    print 'Done!'


if __name__ == '__main__':
    main()
