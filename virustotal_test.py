#!/usr/bin/python3

import os
import requests

DIR = '/var/www/hacked/wordpress/classic/'
APIKEY = os.environ.get('APIKEY_VIRUSTOTAL')

params = {'apikey': APIKEY}
files = {'file': ('setup.py', open('setup.py'), 'rb')}
response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
json_response = response.json()
print(json_response)
print("resource: " + json_response['resource'])

params['resource'] = json_response['resource']
response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
json_response = response.json()
print(json_response)
