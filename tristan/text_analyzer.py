import logging
from nltk import tokenize

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextAnalyzer(object):

    def __init__(self):

        logging.info('Initializing TextAnalyzer')

        self.analyzer = SentimentIntensityAnalyzer()

    def score_relevant_texts(self,relevant_text):

        return {
            subreddit: {
                text:self.__score_text(text)
                for text
                in texts
            }
            for subreddit, texts
            in relevant_text.items()
        }

    def __score_text(self,text):

        avg_score = None
        
        # Converts a chunk of text into individual sentences.
        
        sentences = tokenize.sent_tokenize(text)
        
        if len(sentences) > 0:
        
            total_score = sum([
                self.analyzer.polarity_scores(sentence)['compound']
                for sentence
                in sentences
            ])
            
            avg_score = total_score / len(sentences)
                 
        return avg_score
        
        
