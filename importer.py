#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv, requests

# API conf
API_BASE_URL = 'http://rhizi.local/api'

# Parse data
with open('data.csv', 'rb') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

print "Data: %s rows to export"%len(data)

# GET
for row in data:
    url = API_BASE_URL+"/nodes"
    params = dict(
        id=row["id"]
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()

# POST
for row in data:
    url = API_BASE_URL+"/nodes/"+row["id"]
    params = dict(
        data={ "count" : row["count"] }
    )
    resp = requests.post(url=url, params=params)
    data = resp.json()

