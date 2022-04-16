import json
import boto3

def handler(event, context):

    client = boto3.client('comprehend')
    print("Received event: " + json.dumps(event, indent=2))
    body = event["body"]
    print ("Sentiment analysis on text", body["text"])
    sentiment = client.detect_sentiment(LanguageCode = "en", Text = body["text"])
    return json.dumps(sentiment)


