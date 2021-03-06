import json
import boto3

client = boto3.client('lex-runtime')

def lambda_handler(event, context):
    
    response = client.post_text(
        botName='RupBotTest',
        botAlias='$LATEST',
        userId='admin',
        inputText=event["message"])
        
    return {
        "statusCode": 200,
        "isBase64Encoded": True,
        "headers": {
        'Content-Type':'application/json',    
        'Access-Control-Allow-Origin' : '*'
        },
        "multiValueHeaders": {},
        "body": response
    }