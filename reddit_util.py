import logging
import os

import praw

class RedditUtil(object):
    
    # gather data to analyze
    # TODO create reddit acct
    # TODO get reddit acct keys
    # https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

    def __init__(self,target_subreddits):
        
        logging.info('Initializing Reddit Util')

        if os.exists('praw.ini') is False:

            logging.error('No praw.ini file!')

            exit(1)

        self.reddit = praw.Reddit('tristan')

        self.subreddits = [

            reddit.subreddit(target_subreddit)
            for target_subreddit
            in target_subreddits
            
        ]

    def gather_relevant_text(self,search_term):

        relevant_text = {}

        for subreddit in self.subreddits:

            relevant_text[subreddit.name] = []

            for submission in subreddit.search(search_term,time_filter='week'):

                relevant_text[subreddit.name].append(submission.title)

                for top_level_comment in submission.comments:

                    relevant_text[subreddit.name].append(top_level_comment.body)

        return relevant_text