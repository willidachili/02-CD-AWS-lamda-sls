import json
import boto3

def hello(event, context):

    client = boto3.client('comprehend')
    print("Received event: " + json.dumps(event, indent=2))
    body = event["body"]
    sentiment = client.detect_sentiment(LanguageCode = "en", Text = body["text"])
    return json.dumps(sentiment)

if __name__ == '__main__':

    event = {"body": {
        "text": "The laptop would not boot up when I got it. It would let me get through a few steps of the setup process, then it would become unresponsive and eventually shut down, then restart, then freeze, then repeat, etc. etc. I talked to Apple Support and tried a few different restarts (NVRAM, SMC?), and tried re-installing the OS. None of that worked, so Apple Support concluded that there was probably a hardware issue. Very disappointing. I love Amazon, but they need to do better than this with their renewed electronics. I was so disappointed and frustrated with Amazon that I returned the laptop, and instead of just ordering a replacement from Amazon, I paid a few hundred extra for the same refurbished computer from Apple. I just don't have much confidence in Amazon's renewed program after this experience. I will say, however, that I'm very pleased with Amazon's return policy/process."
    }}

    context = {}
