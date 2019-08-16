#!/usr/bin/env python3
# Sentiment analysis
# SUSHANT KADAM

"""This class does sentiment analysis for the sentence you speak"""
import argparse
import locale
import logging

from aiy.cloudspeech import CloudSpeechClient
from aiy.voice.tts import say
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

""" Some hints sentence that we want to input for the speech recognizer """
def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('goodbye')
    return None

""" Get language of the OS to set the voice/speech accent"""
def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

"""  Listen to a voice and tell if that sentence is positive or negative"""
def main():
    # Logger
    logging.basicConfig(level=logging.DEBUG)

    # Parsing the arguments
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    # SET THE LANGUAGE
    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    
    # Get the client for aiy.cloud
    client = CloudSpeechClient()
    client1 = language.LanguageServiceClient()
    
    
    # Run the loop untill the we say "GOODBYE"
    while True:
        
            
        # Call the cloud Speech to text function to get text from cloud
        text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
        #text1 = u'Hello world'
        document = types.Document(
            content=text,
                type=enums.Document.Type.PLAIN_TEXT)
        
        logging.info('Say something that you want to analyse') 
        # If nothing is been said
        if text is None:
            logging.info('You said nothing.')
            continue
            
        # Display what you said
        logging.info('You said: "%s"' % text)
            
        # Sending the text to sentiment analysis API
        sentiment = client1.analyze_sentiment(document=document).document_sentiment    
        
        # compare the score and decide if it is positive or negative
        if sentiment.score <= -0.25:
            speakThis = 'Negative'
        elif sentiment.score <= 0.25:
            speakThis ='Neutral'
        else:
            speakThis = 'Positive'
        
        # Display what you said
        logging.info('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
           
        #say(speakThis, lang='en-US', volume=80, pitch=130, speed=100, device='default')
           
        #text = text.lower()
##            if 'turn on the light' in text:
##                board.led.state = Led.ON
##            elif 'turn off the light' in text:
##                board.led.state = Led.OFF
##            elif 'blink the light' in text:
##                board.led.state = Led.BLINK
##            elif 'goodbye' in text:
##                break
        if 'goodbye' in text:
            break

if __name__ == '__main__':
    main()
