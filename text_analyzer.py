from nltk import tokenize

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextAnalyzer(object):

    def score_relevant_texts(self,relevant_text):
        
        scores = {}
        
        for subreddit_name, texts in relevant_text.items():
            
            scores[subreddit_name] = {}
            
            for text in texts:
                
                text_score = self.__score_text(text)
                
                scores[subreddit_name][text] = text_score
                
                
                
        return scores

    def __score_text(self,text):

        avg_score = 0
        
        # Converts a chunk of text into individual sentences.
        
        sentences = tokenize.sent_tokenize(content_text)
        
        if len(sentences) > 0:
        
            total_score = 0
            
            # Score each sentence in the text individually.
            
            # The polarity_scores method returns a variety of values, 'compound' is the composite of them all.
            
            for sentence in sentences: 
            
                total_score += self.analyzer.polarity_scores(sentence)['compound']
            
            # Average all the sentence scores.
            
            avg_score = total_score / len(sentences)
                 
        else:
        
            avg_score = None
        
        return avg_score
        
        
