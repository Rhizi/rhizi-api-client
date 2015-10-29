#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv, requests
import argparse

# API conf
API_BASE_URL = 'http://rhizi.local/api'

def parse_data(filename):
    """Parse CSV data from file"""
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    print "Data: %s rows to export"%len(data)
    return data


def get_node(id, params=None):
    """GET method"""

    url = API_BASE_URL+"/nodes/"+id
    resp = requests.get(url=url, params=params)
    return resp.json()


def update_node(id, params=None):
    """Update method"""

    url = API_BASE_URL+"/nodes/"+row["id"]
    resp = requests.post(url=url, params=params)
    return resp.json()

 
if __name__ == '__main__':

    # cli parser
    parser = argparse.ArgumentParser(description='Rhizi Importer with simples options')
    parser.add_argument('filename', action="store", default=None, help='CSV file path' )

    args = parser.parse_args()

    #check if the file exists
    if not os.path.isfile(args.filename) : raise ValueError("File '%s' doesn't exist"%args.filename)

    data = parse_data(args.filename)

    for row in data : 
        params = dict(
            data={ "count" : row["count"] }
        )
        update_node(params)
