#!/usr/bin/env python3
# Sentiment analysis
# SUSHANT KADAM

"""This class does sentiment analysis for the sentence you speak"""
import argparse
import locale
import logging

from aiy.cloudspeech import CloudSpeechClient
from aiy.voice.tts import say

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
    
    # Run the loop untill the we say "GOODBYE"
    while True:
        logging.info('Say something that you want to analyse')
            
        # Call the cloud Speech to text function to get text from cloud
        text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            
        # If nothing is been said
        if text is None:
            logging.info('You said nothing.')
            continue
            
        # Display what you said
        logging.info('You said: "%s"' % text)
            
        # Sending the text to sentiment analysis API
            
        # retun a score
        score = 0
        # compare the score and decide if it is positive or negative
        if score <= -0.25:
            sentiment = "Negative"
        elif score <=0.25:
            sentiment = "Neutral"
        else:
            sentimentstatus = "Positive"
           
        say(sentiment, volume=1, pitch=130, speed=80, device='default')
        # change her locale language, speed
            
            
        text = text.lower()
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
