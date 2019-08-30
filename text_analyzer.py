import logging
from nltk import tokenize

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextAnalyzer(object):

    def __init__(self):

        logging.info('Initializing TextAnalyzer')

        self.analyzer = SentimentIntensityAnalyzer()

    def score_search_results(self,search_results):

        logging.info(f'Scoring {len(search_results)} Search Results')

        for search_result in search_results:

            search_result.sentiment_score = self.__score_text(search_result.target_content)
        
    def __score_text(self,text):

        logging.debug(f'Scoring text: {text}')

        avg_score = None
        
        # Converts a chunk of text into individual sentences.
        
        sentences = tokenize.sent_tokenize(text)
        
        if sentences:
        
            # The polarity_scores method returns a variety of values, 'compound' is the composite of them all.
            sentence_scores = [
                self.analyzer.polarity_scores(sentence)['compound']
                for sentence
                in sentences
            ]
            
            # Average all the sentence scores.
            avg_score = sum(sentence_scores) / len(sentence_scores)
                 
        logging.debug(avg_score)
        
        return avg_score