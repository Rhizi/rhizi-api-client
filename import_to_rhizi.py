#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv
import argparse
from client import RhiziAPIClient

def parse_data(filename):
    """Parse CSV data from file"""
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    print "Data: %s rows to export"%len(data)
    return data

if __name__ == '__main__':

    # cli parser
    parser = argparse.ArgumentParser(description='Rhizi Importer with simples options')
    parser.add_argument('filename', action="store", default=None, help='CSV file path' )
    parser.add_argument('--base-url', default='http://localhost:8080', help='Base URL for the API')
    parser.add_argument('--user', default=None, help='Username')
    parser.add_argument('--password', default=None, help='pasword' )

    args = parser.parse_args()

    # init Client API
    print args.base_url
    client = RhiziAPIClient(args.base_url)

    # log user in
    client.user_login(args.user, args.password)
    print client,

    #check if the file exists
    if not os.path.isfile(args.filename) : raise ValueError("File '%s' doesn't exist"%args.filename)

    # parse data
    data = parse_data(args.filename)



    # update nodes
    # for row in data :
    #     params = dict(
    #         data={ "count" : row["count"] }
    #     )
    #     update_node(params)
