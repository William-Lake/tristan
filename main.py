from argparse import ArgumentParser
import json
import logging
import os
import time
import traceback

from bottle import route, run, request, response

from reddit_util import RedditUtil
from text_analyzer import TextAnalyzer

def validate_params(subreddits,search_term):

    logging.info('Validating params.')
    
    if subreddits is None or search_term is None:

        response.status = 400

        if subreddits is None and search_term is None:

            return 'Neither subreddits nor a search term was provided.'

        elif subreddits is None:

            return "One or more subreddits weren't provided."

        else:

            return "A search term wasn't provided."

    return None

def gather_params():

    logging.info('Gathering Params.')
    
    request_json = request.json

    try:
    
        subreddits = request_json['subreddits']
    
    except KeyError as e:

        logging.error('KeyError while trying to gather subreddits from request.')

        subreddits = None
    
    # TODO Validate the subreddits exist: https://praw.readthedocs.io/en/latest/code_overview/reddit/subreddits.html?highlight=search%20subreddits#praw.models.Subreddits.search_by_name
    
    try:

        search_term = request_json['search_term']

    except KeyError as e:

        logging.error('KeyError while trying to gather search term from request.')

        search_term = None
    
    return subreddits, search_term

@route('/tristan/<search_term>/<subreddits>')
def tristan(search_term,subreddits):
    
    logging.info('Received request.')

    # subreddits, search_term = gather_params()

    subreddits = subreddits.strip().split(';')

    # error_message = validate_params(subreddits,search_term)

    # if error_message is not None: 
        
    #     logging.info(f'There was an issue with the params, returning error message: {error_message}.')

    #     return error_message
    
    logging.info(f'Gathering data from {", ".join(subreddits)} using {search_term}.')

    reddit_util = RedditUtil(subreddits)
    
    search_results = reddit_util.gather_search_results(search_term)

    logging.info('Analyzing data.')

    text_analyzer = TextAnalyzer()
    
    text_analyzer.score_search_results(search_results)

    logging.info('Averaging Scores.')

    search_result_scores = [
        search_result.sentiment_score
        for search_result
        in search_results
    ]

    reddit_scores = [
        search_result.score
        for search_result
        in search_results
    ]

    avg_score = sum(search_result_scores) / len(search_result_scores)

    avg_reddit_score = sum(reddit_scores) / len(reddit_scores)

    logging.info('Constructing return json.')

    out_data = {
        'search_term':search_term,
        'subreddits':subreddits,
        'avg_score':avg_score,
        'avg_reddit_score':avg_reddit_score,
        'subreddit_data':{}
    }

    subreddit_names = set([
        search_result.source_subreddit
        for search_result
        in search_results
    ])

    for subreddit_name in subreddit_names:

        out_data['subreddit_data'][subreddit_name] = []

        related_search_results = [
            search_result
            for search_result
            in search_results
            if search_result.source_subreddit == subreddit_name
        ]

        for related_search_result in related_search_results:

            search_result_info = {
                'sentiment_score':related_search_result.sentiment_score,
                'target_content':related_search_result.target_content,
                'reddit_score':related_search_result.score,
                'upvote_ratio':(related_search_result.upvote_ratio if related_search_result.is_submission else 'N/A'),
                'post_or_comment':('post' if related_search_result.is_submission else 'comment'),
                'author':related_search_result.author,
                'source_subreddit':related_search_result.source_subreddit,
                'created_utc':related_search_result.created_utc,
                'permalink':related_search_result.permalink
            }

            out_data['subreddit_data'][subreddit_name].append(search_result_info)

    response.set_header('Content-Type','application/json')
    
    return json.dumps(out_data,indent=4)
    
def gather_args():
    '''
    Gathers the command line args provdied at startup via argparse.
    '''

    # TODO Consider providing praw.ini here
    
    arg_parser = ArgumentParser('Tristan')
    
    arg_parser.add_argument('host',default='localhost')
    
    arg_parser.add_argument('port',type=int,default=8080)
    
    args = arg_parser.parse_args()
    
    return args.host, args.port

if __name__ == '__main__':

    # TODO Create functionality for multiple searches per request

    logging.basicConfig(level=logging.INFO)
    
    host, port = gather_args()

    if os.path.exists('praw.ini') is False:

        logging.error('No praw.ini file in current directory!')

        exit(1)
    
    run(host=host, port=port)