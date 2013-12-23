#!/usr/bin/env python

import argparse
import csv
import json


# The data in the huge CSVs are as follows:
# id,sender,message,date,geolat,geolon
# ComStat (currently) expects lat/lon to be the first two columns

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweets_csv',
                        type=argparse.FileType('r'),
                        help='The huge CSV file with tweet data')
    parser.add_argument('output_csv',
                        type=argparse.FileType('w'),
                        help='The CSV file to write output to')
    return parser.parse_args()

def main():
    args = parse_args()

    infile = args.tweets_csv
    outfile = args.output_csv

    print 'Converting...'
    count = 0
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for csv_line in reader:
        count += 1
        out_line = csv_line[4:6] + csv_line[0:4]
        writer.writerow(out_line)
    print 'Ran through %d tweets!' % count

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

