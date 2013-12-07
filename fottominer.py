#!/usr/bin/env python

import argparse
import json

from twython import Twython

from authmgr import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', metavar='FILENAME',
                        dest='output_file',
                        help='The file in which result data should be stored')
    parser.add_argument('search_string')

    return parser.parse_args()


def main():
    args = parse_args()

    print 'Loading keys...'
    auth_dict = load_oauth_keys()

    print 'Acquiring access token...'
    access_token = get_access_token(auth_dict)

    print 'Authenticating with access token...'
    twitter = Twython(auth_dict['CONSUMER_KEY'], access_token=access_token)

    print 'Searching...'
    result = twitter.search(q=args.search_string, count=100)
    
    outfile_name = args.output_file or 'result.json'

    print 'Saving result JSON to %s' % outfile_name
    outfile = file(outfile_name, 'w')
    outfile.write(json.dumps(result, indent=2))

    print 'Done!'


if __name__ == '__main__':
    main()
