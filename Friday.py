#!/usr/bin/env python3
# Sentiment analysis on google AiY using Google Cloud Sentiment analysis API
# SUSHANT KADAM

"""This code does sentiment analysis for the sentence you speak"""
import argparse
import locale
import logging
from aiy.cloudspeech import CloudSpeechClient
from aiy.board import Board, Led # TO CONTROL GPIO and LED
from aiy.voice.tts import say # FUNCTION TO MAKE AiY Speak
from google.cloud import language # SENTIMENT ANALYSIS API
from google.cloud.language import enums # Sentiment DataStructures
from google.cloud.language import types 

""" CHANGE THE CONSTANTS HERE """
ASSITANT_VOLUME = 70
POSITIVE = "Expresses Positivity"
NEGATIVE = "Expresses Negativity"
NEUTRAL = "Expresses Neutrality"
LOW_CUTOFF = -0.25
HIGH_CUTOFF = 0.25 
STOPAT = 3
GOODBYE = 'goodbye'

""" Here we put hints sentence that we want to input for the speech recognizer to make its life easier"""
def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('goodbye')
    return None

""" Get language of the OS to set the voice/speech accent as per the system"""
def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

"""  Main Function """
def main():
    
    # Creating a logger
    logging.basicConfig(level=logging.DEBUG)

    # Parsing the arguments, in our case its the system language
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    # SEE THE LOCALE LANGUAGE(Accent)
    logging.info('Initializing the locale language %s...', args.language)
    hints = get_hints(args.language)
    
    # Create the client for aiy.CloudToSpeech API to convert the speech to text
    cstclient = CloudSpeechClient()
    # Create the client for sentiment analysis API
    sentimentClient = language.LanguageServiceClient()
    
    # This counter is used check if something is said to the AiY, or break if nothing is said 3 times
    breakCount = 0
    # To Control the board LEDs
    with Board() as board:
        
        # Run the loop untill the we say "GOODBYE" or nothing is said 3 times
        while True:
        
            # LED ON to show Aiy is listening
            board.led.state = Led.ON
            
            # Call the cloud Speech to text recognize function to get text from the API
            # Language code is Indian to understand our accent better
            text = cstclient.recognize(language_code=args.language,
                                    hint_phrases=hints)
        
            # LED OFF to indicate the some activity is happening
            board.led.state = Led.BLINK
            
            logging.info('Say something that you want to analyse') 
        
            # If nothing has been said
            if text is None:
                board.led.state = Led.OFF
                breakCount = breakCount + 1
                # break if nothing is said 3 times
                if breakCount == STOPAT:
                    logging.info('You said nothing. "%d" times. GOODBYE!' % breakCount)
                    say("Good bye", lang='en-GB', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')
                    break
                
                logging.info('You said nothing. "%d" times' % breakCount)
                continue
            else:
                breakCount = 0 # RESET the break count back to 0
            
            # To get out of the loop say GOODBYE
            if GOODBYE in text:
                board.led.state = Led.OFF
                logging.info('Good bye!')
                say("Good bye", lang='en-GB', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')
                break

            # Display what you said
            logging.info('You said: "%s"' % text)
            board.led.state = Led.BLINK
            
            # Add the text to the document which is then sent to the sentiment analysis function
            document = types.Document(
                content=text,
                    type=enums.Document.Type.PLAIN_TEXT)
        
            # Sending the text to sentiment analysis API analyze_sentiment function
            # A score is returned back by the function, it also has weighted score called magnitude
            sentiment = sentimentClient.analyze_sentiment(document=document).document_sentiment    
        
            # compare the score and decide if it is positive or negative
            # Add the sentimentmagnitude to the conditions to get better sentiments values
            # We assume these constants(ex 0.25), to be our base to find the nature of the sentiment
            if sentiment.score <= LOW_CUTOFF:
                speakThis = NEGATIVE 
            elif sentiment.score <= HIGH_CUTOFF:
                speakThis = NEUTRAL
            else:
                speakThis = POSITIVE
        
            # Log score coming from the API
            logging.info('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
            # Log the nature of the sentiment
            logging.info('Sentiment seems to be "%s"' % speakThis)
            board.led.state = Led.OFF
        
            # Speak the sentiment # Accent is US (as en-IN is not available for AiY)  
            say(speakThis, lang='en-US', volume=ASSITANT_VOLUME, pitch=95, speed=100, device='default')

if __name__ == '__main__':
    main()