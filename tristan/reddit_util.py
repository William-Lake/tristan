import logging
import os

import praw
from tqdm import tqdm

class RedditUtil(object):
    
    # gather data to analyze
    def __init__(self):
        
        logging.info('Initializing Reddit Util')

        if os.path.exists('praw.ini') is False:

            logging.error('No praw.ini file!')

            exit(1)

        # TODO Allow the user to determine this via args
        self.reddit = praw.Reddit('tristan_bot') 

    def gather_relevant_text(self,subreddits,search_term,time_filter):

        relevant_text = {}

        for subreddit in tqdm(subreddits,leave=False,desc='Subreddits'):

            relevant_text[subreddit] = []

            submissions = subreddit.search(search_term,time_filter=time_filter)

            # TODO Allow the user to choose the filter length via args
            for submission in tqdm(submissions,leave=False,desc=f'{subreddit} results'):

                # Is this what you want?
                if search_term in submission.title:

                    relevant_text[subreddit].append(submission.title)

                    for top_level_comment in tqdm(submission.comments, leave=False, desc='Submission Comments'):

                        # Happens when the MoreComments object comes up
                        # TODO Determine if you want to use the additional comments and better handle this
                        try:

                            relevant_text[subreddit].append(top_level_comment.body)

                        except:

                            pass

        return relevant_text


    def gather_subreddits(self,query_subreddits,subreddit_cache):

        subreddits = []

        for subreddit in query_subreddits:

            if subreddit not in subreddit_cache.keys():

                subreddit_cache[subreddit] = self.reddit.subreddit(subreddit)

            subreddits.append(subreddit_cache[subreddit])        

        return subreddits