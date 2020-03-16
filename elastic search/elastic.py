#FWpgAhLrOEQFMw9o3MCIDPJWFHNYhyH0WbEovt3Z
import boto3
import json
import decimal
from datetime import datetime
import requests

header={'Content-Type': 'application/json'}

with open('data.json') as json_file: 
	data = json.load(json_file) 

	temp = data['businesses']
	count=2
	for business in temp:
		url='ELASTIC_SEARCH_URL/restaurants/_doc/'+str(count)
		print(url)
		data={"id":business['id'], "cuisine":business['categories'][0]['title']}
		data_json=json.dumps(data)
		r=requests.put(url, headers=header, data=data_json)
		response=r.text
		print(response)
		count+=1