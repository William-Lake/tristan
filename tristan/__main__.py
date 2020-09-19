from argparse import ArgumentParser
from datetime import datetime
import json
import logging
import time

from reddit_util import RedditUtil
from text_analyzer import TextAnalyzer

def gather_args():
    
    arg_parser = ArgumentParser('Tristan')
    
    arg_parser.add_argument('--do_write_out',action='store_true',help='Include if you want the results written to a json file.')
    
    arg_parser.add_argument('search_term',help="The term/phrase you're searching for. If there's spaces wrap it in double quotes.")
    
    arg_parser.add_argument('subreddits',nargs='+',help='A list of one or more subreddits to scan for the search term.')
    
    args = arg_parser.parse_args()
    
    return args.do_write_out, args.search_term, args.subreddits

if __name__ == '__main__':

    # TODO Create functionality for multiple searches per execution

    logging.basicConfig(level=logging.INFO)

    '''
    gather user search term
    gather data to analyze
    analyze data
    write to json
    print results
    '''

    # gather user search term
    do_write_out, search_term, subreddits = gather_args()

    # gather data to analyze
    reddit_util = RedditUtil(subreddits)
    
    relevant_text = reddit_util.gather_relevant_text(search_term)

    # analyze data
    
    text_analyzer = TextAnalyzer()
    
    scores = text_analyzer.score_relevant_texts(relevant_text)
    
    avg_scores = {}

    logging.info('Calculating Average Scores')

    for subreddit_name, text_scores in scores.items():
     
        if text_scores.values():

            avg_scores[subreddit_name] = sum(text_scores.values()) / len(text_scores.values())

    if avg_scores:

        final_avg_score = sum(avg_scores.values()) / len(avg_scores.values())

    else:

        final_avg_score = 'No data found to create scores from!'
    
    if do_write_out:

        logging.info('Writing collected data to file')
        
        out_data = {
            'search_term':search_term,
            'subreddits':subreddits,
            'avg_score':final_avg_score
        }

        subreddit_data = {}
        
        for subreddit_name, text_scores in scores.items():

            subreddit_data[subreddit_name] = {
                'avg_score':avg_scores[subreddit_name],
                'data':text_scores
            }

        out_data['subreddit_data'] = subreddit_data
            
        file_name = f'{search_term.replace(" ","_")}_{datetime.today().__str__()}.json'

        with open(file_name,'w+') as out_file:
            
            out_file.write(json.dumps(out_data,indent=4))

    print(f'"{search_term}": {final_avg_score}')