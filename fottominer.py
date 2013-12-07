#!/usr/bin/env python

import argparse
import json
import urlparse

from twython import Twython

from authmgr import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', metavar='FILENAME',
                        dest='output_file', type=argparse.FileType('w'),
                        help='The file in which result data should be stored')
    parser.add_argument('search_string', help='String to search for')
    parser.add_argument('num_pages', type=int,
                        help='Number of search result pages to read')

    return parser.parse_args()


class FottoMiner(object):

    def __init__(self):
        print 'Requesting access token...'
        auth_dict = load_oauth_keys()
        access_token = get_access_token(auth_dict)

        print 'Authenticating with access token...'
        twitter = Twython(auth_dict['CONSUMER_KEY'], access_token=access_token)
        self.twitter = twitter

    def next_page_qs_to_args(self, next_page_qs):
        """
        This method converts the next_page string present in Twitter API search
        results into a dict of search parameters for the next page.
        """

        # Remove the leading question mark, which could mess up our parameters
        if next_page_qs[0] == '?':
            next_page_qs = next_page_qs[1:]

        parsed_qs = urlparse.parse_qs(next_page_qs)

        # The parsed values are stored inside arrays - take them out of these
        parameters = {}
        for key in parsed_qs.keys():
            parameters[key] = parsed_qs[key][0]

        return parameters

    def get_tweets(self, search_string, num_pages):
        twitter = self.twitter
        cur_page = 0
        search_args = {
            'q': search_string,
            'count': 10
        }
        tweets = []

        for i in range(cur_page, num_pages):
            print 'Getting page %d/%d' % (cur_page + 1, num_pages)
            result = twitter.search(**search_args)
            tweets += result['statuses']

            metadata = result['search_metadata']
            if metadata.has_key('next_results'):
                next_page_qs = result['search_metadata']['next_results']
                search_args = self.next_page_qs_to_args(next_page_qs)

                cur_page += 1
            else:
                print 'Ran out of pages -- stopping search here!'
                break

        return tweets


def main():
    args = parse_args()
    miner = FottoMiner()

    print 'Searching...'
    result = miner.get_tweets(args.search_string, args.num_pages)
    print 'Retrieved %d tweets' % len(result)
    
    outfile = args.output_file or file('result.json', 'w')

    outfile.write(json.dumps(result, indent=2))
    outfile.close()

    print 'Done!'


if __name__ == '__main__':
    main()
