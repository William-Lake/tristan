import logging

import praw

class SearchResult:

    def __init__(self,source_subreddit,target_content,author,created_utc,permalink,score,upvote_ratio=None,is_submission=False):

        self.source_subreddit = source_subreddit

        self.target_content = target_content

        self.author = author

        self.created_utc = created_utc

        self.permalink = permalink

        self.score = score

        self.upvote_ratio = upvote_ratio

        self.is_submission = is_submission

        self.sentiment_score = None

class RedditUtil(object):
    
    # gather data to analyze
    def __init__(self,target_subreddits):

        # TODO Determine way to let main.py know if the praw.i
        
        logging.info('Initializing Reddit Util')

        # TODO Allow the user to determine this via params
        self.reddit = praw.Reddit('tristan_bot')

        self.subreddits = []

        for target_subreddit in target_subreddits:

            logging.info(f'Gathering subreddit object for r/{target_subreddit}.')

            self.subreddits.append(self.reddit.subreddit(target_subreddit))

    def gather_search_results(self,search_term,time_filter):

        logging.info(f'Gathering search results for {search_term}.')

        search_results = []

        for subreddit in self.subreddits:

            logging.debug(f'Gathering text from r/{subreddit.display_name}')

            # TODO Allow the user to choose the filter length via args
            for submission in subreddit.search(search_term,time_filter=time_filter):

                if search_term in submission.title:

                    logging.debug(f'Gathering text from submission "{submission.title}"')

                    search_result = SearchResult(subreddit.display_name,submission.title,submission.author.name,submission.created_utc,submission.permalink,submission.score,upvote_ratio=submission.upvote_ratio,is_submission=True)

                    search_results.append(search_result)

                    for top_level_comment in submission.comments:

                        # Happens when the MoreComments object comes up
                        # TODO Determine if you want to use the additional comments and better handle this
                        try:

                            if top_level_comment.author.name == 'AutoModerator': continue

                            comment_search_result = SearchResult(subreddit.display_name,top_level_comment.body,top_level_comment.author.name,top_level_comment.created_utc,top_level_comment.permalink,top_level_comment.score)

                            search_results.append(comment_search_result)

                        except:

                            logging.info('Hit a MoreComments object')

                            continue

        return search_results