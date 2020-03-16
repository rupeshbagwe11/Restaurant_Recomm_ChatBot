
#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from datetime import datetime
import requests
from MyYelpAPI import *


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


#indian - indpak, chinese -chinese, french -french, american - newamerican, italian - italian

business_id = 'BUSINESS_ID'

API_KEY = getYelpAPIKey()
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

PARAMETERS = {'term': 'food',
             'limit': 50,
             'offset': 0,
             'radius': 5000,
             'categories': 'newamerican',
             'location': 'Manhattan'}

response = requests.get(url = ENDPOINT,
                        params = PARAMETERS,
                        headers = HEADERS)

restaurant_data = response.json()


dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="DYNAMO_DB_URL")

table = dynamodb.Table('restaurants')

print(table)

i=0
for resta in restaurant_data['businesses']:
     if  i == 25:	
         break

     BusinessID = resta['id']
     Cuisine = 'american'
     Name = resta['name']
     Address = resta['location']['display_address'][0]  + ' ' + resta['location']['display_address'][1]
     Coordinates = str(resta['coordinates']['latitude']) + ' ' + str(resta['coordinates']['longitude'])
     NumberofReviews = str(resta['review_count'])
     Rating = str(resta['rating'])
     ZipCode = str(resta['location']['zip_code'])
     now = datetime.now()
     current_time = now.strftime("%m-%d-%Y %H:%M:%S")
     InsertedAtTimestamp = current_time

     item = {
         'BusinessID': BusinessID,
         'Cuisine': Cuisine,
         'Name': Name,
         'Address': Address,
         'Coordinates': Coordinates,
         'NumberofReviews': NumberofReviews,
         'Rating': Rating,
         'ZipCode': ZipCode,
         'InsertionTimeStamp': InsertedAtTimestamp,
     }
     #print(Item)
     # response = table.put_item(
     #     Item={
     #     'BusinessID': BusinessID,
     #     'Cuisine': Cuisine,
     #     'Name': Name,
     #     'Address': Address,
     #     'Coordinates': Coordinates,
     #     'NumberofReviews': NumberofReviews,
     #     'Rating': Rating,
     #     'ZipCode': ZipCode,
     #     'InsertionTimeStamp': InsertedAtTimestamp,
     #         }
     # )

     response = table.put_item(Item=item)

     print("PutItem succeeded:")
     print(json.dumps(response, indent=4, cls=DecimalEncoder))
     i=i+1










