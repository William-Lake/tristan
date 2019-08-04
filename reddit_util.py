import logging
import os

import praw

class RedditUtil(object):
    
    # gather data to analyze
    def __init__(self,target_subreddits):
        
        logging.info('Initializing Reddit Util')

        if os.path.exists('praw.ini') is False:

            logging.error('No praw.ini file!')

            exit(1)

        # TODO Allow the user to determine this via args
        self.reddit = praw.Reddit('tristan_bot') 

        self.subreddits = [

            self.reddit.subreddit(target_subreddit)
            for target_subreddit
            in target_subreddits
            
        ]

    def gather_relevant_text(self,search_term):

        logging.info(f'Gathering relevant text for {search_term}')

        relevant_text = {}

        for subreddit in self.subreddits:

            logging.debug(f'Gathering text from r/{subreddit.display_name}')

            relevant_text[subreddit.display_name] = []

            # TODO Allow the user to choose the filter length via args
            for submission in subreddit.search(search_term,time_filter='week'):

                if search_term in submission.title:

                    logging.debug(f'Gathering text from submission "{submission.title}"')

                    relevant_text[subreddit.display_name].append(submission.title)

                    for top_level_comment in submission.comments:

                        # Happens when the MoreComments object comes up
                        # TODO Determine if you want to use the additional comments and better handle this
                        try:

                            relevant_text[subreddit.display_name].append(top_level_comment.body)

                        except:

                            pass

        return relevant_text