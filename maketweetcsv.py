#!/usr/bin/env python

import argparse
import csv
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweets_file',
                        type=argparse.FileType('r'),
                        help='The file containing tweet data')
    parser.add_argument('csv_file',
                        type=argparse.FileType('w'),
                        help='The CSV file that will be written to')
    return parser.parse_args()


def load_tweets_from_file(infile):
    tweets_json = infile.read()
    return json.loads(tweets_json)


def get_geolocated_tweets(tweets):
    geolocated_tweets = [t for t in tweets if t['coordinates']]
    return geolocated_tweets


def tweets_to_2d_array(tweet_dicts):
    tweet_array = []

    for tweet in tweet_dicts:
        row = []

        coordinates = tweet['coordinates']
        row += coordinates['coordinates'] # Shove the lat/long in there
        row.append(tweet['retweet_count'])

        tweet_array.append(row)

    return tweet_array


def main():
    args = parse_args()

    print 'Loading tweets...'
    tweets = load_tweets_from_file(args.tweets_file)

    print 'Filtering out non-geolocated tweets...'
    geo_tweets = get_geolocated_tweets(tweets)
    print 'Got %d geolocated tweets (out of %d)' % (len(geo_tweets), len(tweets))
    tweets = geo_tweets

    tweets2d = tweets_to_2d_array(tweets)

    print 'Writing CSV...'
    writer = csv.writer(args.csv_file)
    for row in tweets2d:
        writer.writerow(row)

    args.csv_file.close()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
