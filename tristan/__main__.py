from argparse import ArgumentParser
from datetime import datetime
import json
import logging
import time

from bottle import post, request, run, abort, response
from tqdm import tqdm

from reddit_util import RedditUtil
from text_analyzer import TextAnalyzer


def gather_subreddit_data(scores,avg_scores):

    return {
        subreddit.display_name: {
            'avg_score':avg_scores[subreddit.display_name] if subreddit.display_name in avg_scores.keys() else "No Scores!",
            'data':text_scores
        }
        for subreddit, text_scores
        in scores.items()
    }

def gather_score_data(scores):

    avg_scores = {}

    for subreddit, text_scores in scores.items():
    
        scores = [s for s in text_scores.values() if s is not None]

        if scores:

            avg_scores[subreddit.display_name] = sum(scores) / len(scores)

    if avg_scores:

        final_avg_score = sum(avg_scores.values()) / len(avg_scores.values())

    else:

        final_avg_score = 'No data found to create scores from!'    

    return avg_scores, final_avg_score

def gather_args():

    arg_parser = ArgumentParser()

    arg_parser.add_argument('--port',type=int,nargs='?',default=9010,help='The port to run tristan on.')

    return arg_parser.parse_args().port

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    port = gather_args()

    text_analyzer = TextAnalyzer()

    reddit_util = RedditUtil()

    @post('/tristan')
    def search():

        search_json = request.json

        if search_json:

            if 'queries' in search_json.keys():

                results = []

                subreddit_cache = {}

                for query in tqdm(search_json['queries'],leave=False,desc='Queries'):

                    result = {
                        'query':query
                    }

                    if 'subreddits' not in query.keys():

                        result['error'] = 'Query doesn\'t contain subreddits.'

                    elif 'search_text' not in query.keys():

                        result['error'] = 'Query doesn\'t contain search_text.'

                    else:

                        subreddits = reddit_util.gather_subreddits(query['subreddits'],subreddit_cache)

                        time_filter = query['time_filter'].lower() if 'time_filter' in query.keys() and query['time_filter'].lower() in ['all','day','hour','month','week','year'] else 'week'

                        relevant_texts = reddit_util.gather_relevant_text(subreddits,query['search_text'],time_filter)

                        scores = text_analyzer.score_relevant_texts(relevant_texts)
                        
                        avg_scores, final_avg_score = gather_score_data(scores)

                        subreddit_data = gather_subreddit_data(scores,avg_scores)

                        result.update({
                            'avg_score':final_avg_score,
                            'avg_scores':avg_scores,
                            'subreddit_data':subreddit_data
                        })
                        
                    results.append(result)  

                response.set_header('Content-Type','application/json')

                return json.dumps(results,indent=4)
        else:

            abort(400,'Something\'s up, doc. Probably a json issue.')

    run(port=port)
    