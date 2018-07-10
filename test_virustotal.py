#!/usr/bin/python3

import pyclamd
import os
import requests

DIR = '/var/www/hacked/wordpress/classic/'

params = {'apikey': 'a4f93846f3ebaa63de2806ea0e08c5010872cf08f69ca0450abe6292d55b6b4f'}
files = {'file': ('setup.py', open('setup.py'), 'rb')}
response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
json_response = response.json()
print(json_response)
print("resource: " + json_response['resource'])

params['resource'] = json_response['resource']
response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
json_response = response.json()
print(json_response)



