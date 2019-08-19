#!/usr/bin/env python3
# Sentiment analysis on google AiY using Google Cloud Sentiment analysis API
# SUSHANT KADAM

"""This class does sentiment analysis for the sentence you speak"""
import argparse
import locale
import logging

from aiy.cloudspeech import CloudSpeechClient
#from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.board import Board, Led
from aiy.voice.tts import say
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

""" CHANGE THE VOLUME OF THE ASSISTANT HERE """
ASSITANT_VOLUME = 60

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

    # SEE THE LOCALE LANGUAGE(Accent)
    logging.info('Initializing the locale language %s...', args.language)
    hints = get_hints(args.language)
    
    # Create the client for aiy.cloud
    cstclient = CloudSpeechClient()
    # Create the client for sentiment analysis
    sentimentClient = language.LanguageServiceClient()
    
    # Check if something is said, or break if nothing is said 3 times
    breakCount = 0
    with Board() as board:
        # Run the loop untill the we say "GOODBYE"
        while True:
        
            # LED ON to show we are listening
            board.led.state = Led.ON   
            # Call the cloud Speech to text function to get text from cloud
            text = cstclient.recognize(language_code=args.language,
                                    hint_phrases=hints)
        
            # LED OFF to indicate the some activity is happening
            board.led.state = Led.BLINK
            
            logging.info('Say something that you want to analyse') 
        
            # If nothing is been said
            if text is None:
                board.led.state = Led.OFF
                breakCount = breakCount + 1
                # break if nothing is said 3 times
                if breakCount == 3:
                    logging.info('You said nothing. "%d" times. GOODBYE!' % breakCount)
                    say("Good bye", lang='en-GB', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')
                    break
                logging.info('You said nothing. "%d" times' % breakCount)
                continue
            else:
                breakCount = 0 # RESET the break count back to 0
            
            # To get out of the while loop say GOODBYE
            if 'goodbye' in text:
                board.led.state = Led.OFF
                logging.info('Good bye!')
                say("Good bye", lang='en-GB', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')
                break

            if 'party time' in text:
                board.led.state = Led.BLINK
                continue
            
            # Display what you said
            logging.info('You said: "%s"' % text)
            board.led.state = Led.BLINK
            
            document = types.Document(
                content=text,
                    type=enums.Document.Type.PLAIN_TEXT)
        
            # Sending the text to sentiment analysis API
            sentiment = sentimentClient.analyze_sentiment(document=document).document_sentiment    
        
            # compare the score and decide if it is positive or negative
            # Add the sentimentmagnitude to the conditions to get better sentiments values
            if sentiment.score <= -0.25:
                speakThis = 'Expresses Negativity'
            elif sentiment.score <= 0.25:
                speakThis ='Expresses Neutrality'
            else:
                speakThis = 'Expresses Positivity'
        
            # Display what you said
            logging.info('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
            logging.info('Sentiment seems to be "%s"' % speakThis)
            board.led.state = Led.OFF
        
            # SPEAK THE SENTIMENT # Accent is BRITISH   
            say(speakThis, lang='en-US', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')
            
            

if __name__ == '__main__':
    main()
