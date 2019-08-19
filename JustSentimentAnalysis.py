#imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

while True:
    # The text to analyze
    line = input("Enter text :")
    text = line
    document = types.Document(
                content=text,
                    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    if sentiment.score <= -0.25:
        speakThis = 'Negative'
    elif sentiment.score <= 0.25:
        speakThis ='Neutral'
    else:
        speakThis = 'Positive'

    print("Sentiment" , speakThis)
    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


