from argparse import ArgumentParser
import json
import logging
import time

from reddit_util import RedditUtil
from text_analyzer import TextAnalyzer

def gather_params():
    
    request_json = request.json
    
    #TODO Try/except around these re: KeyErrors
    subreddits = request_json['subreddits']
    
    #TODO Validate subreddits provided
    
    search_term = request_json['search_term']
    
    #TODO Validate search term
    
    return subreddits, search_term

@route('/tristan')
def analyze():
    
    subreddits, search_term = gather_params()
    
    # gather data to analyze
    reddit_util = RedditUtil(subreddits)
    
    relevant_text = reddit_util.gather_relevant_text(search_term)

    # analyze data
    
    text_analyzer = TextAnalyzer()
    
    scores = text_analyzer.score_relevant_texts(relevant_text)
    
    avg_scores = {}

    logging.info('Calculating Average Scores')

    for subreddit_name, text_scores in scores.items():
     
        avg_score = sum(text_scores.values()) / len(text_scores.values())
        
        avg_scores[subreddit_name] = avg_score
        
    final_avg_score = sum(avg_scores.values()) / len(avg_scores.values())
    
    # TODO Simplify this process

    out_data = {}
        
    out_data['search_term'] = search_term
        
    out_data['subreddits'] = subreddits
        
    out_data['avg_score'] = final_avg_score
        
    out_data['subreddit_data'] = {}
        
    for subreddit_name, text_scores in scores.items():
            
        out_data['subreddit_data'][subreddit_name] = {}
            
        out_data['subreddit_data'][subreddit_name]['avg_score'] = avg_scores[subreddit_name]
            
        out_data['subreddit_data'][subreddit_name]['data'] = text_scores
            
    response.set_header('Content-Type','application/json')
    
    response.body = json.dumps(out_data,indent=4)
    
def gather_args():
    
    arg_parser = ArgumentParser('Tristan')
    
    arg_parser.add_argument('host',default='localhost')
    
    arg_parser.add_argument('port',type=int,default=8080)
    
    args = arg_parser.parse_args()
    
    return args.host, args.port

if __name__ == '__main__':

    # TODO Create functionality for multiple searches per request

    logging.basicConfig(level=logging.INFO)
    
    host, port = gather_args()
    
    run(host=host, port=port)