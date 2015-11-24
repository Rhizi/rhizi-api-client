#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv
import argparse
from rhizi_client import RhiziAPIClient, set_debugging

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
    parser.add_argument('--password', default=None, help='Password' )
    parser.add_argument('--rz-doc-name', default="Welcome to Rhizi", help='Name of the document to update' )
    parser.add_argument('--verbose', default=False, help='Show / hide logs' )

    args = parser.parse_args()

    # verbose mode


    # init Client API
    print args.base_url
    client = RhiziAPIClient(args.base_url, args.user, args.password, debug=args.verbose)

    #check if the file exists
    if not os.path.isfile(args.filename) : raise ValueError("File '%s' doesn't exist"%args.filename)

    # parse data
    data = parse_data(args.filename)

    # update nodes
    client.create_node(args.rz_doc_name, "Muttons")

    # for row in data :
    #     params = dict(
    #         data={ "count" : row["count"] }
    #     )
    #     update_node(params)
