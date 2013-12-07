
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
