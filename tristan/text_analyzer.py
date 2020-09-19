import logging

from textblob import TextBlob



class TextAnalyzer(object):

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

        blob = TextBlob(text)

        sentences = blob.sentences

        if sentences:

            total_score = sum([
                sentence.sentiment.polarity
                for sentence
                in sentences
            ])

            avg_score = total_score / len(sentences)

        return avg_score