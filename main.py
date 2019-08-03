from argparser import ArgumentParser
import json
import time

from reddit_util import RedditUtil
from text_analyzer import TextAnalyzer

def gather_args():
    
    arg_parser = ArgumentParser('RedditReview')
    
    arg_parser.add_argument('--write_out',action='store_true')
    
    arg_parser.add_argument('search_term')
    
    arg_parser.add_argument('subreddits',nargs='+')
    
    args = arg_parser.parse_args()
    
    return args.write_out, args.search_term, args.subreddits


if __name__ == '__main__':

    '''
    gather user search term
    gather data to analyze
    analyze data
    write to json
    print results
    '''

    # gather user search term
    write_out, search_term, subreddits = gather_args()

    # gather data to analyze
    reddit_util = RedditUtil(subreddits)
    
    relevant_text = reddit_util.gather_relevant_text(search_term)

    # analyze data
    
    text_analyzer = TextAnalyzer()
    
    scores = text_analyzer.score_relevant_texts(relevant_texts)
    
    avg_scores = {}

    for subreddit_name, text_scores in scores.items():
     
        avg_score = sum(text_scores.values()) / len(text_scores.values())
        
        avg_scores[subreddit_name] = avg_score
        
    final_avg_score = sum(avg_scores.values()) / len(avg_scores.values())
    
    if write_out:
        
        out_data = {}
        
        out_data['search_term'] = search_term
        
        out_data['subreddits'] = subreddits
        
        out_data['avg_score'] = final_avg_score
        
        out_data['subreddit_data'] = {}
        
        for subreddit_name, text_scores in scores.items():
            
            out_data['subreddit_data'][subreddit_name] = {}
            
            out_data['subreddit_data'][subreddit_name]['avg_score'] = avg_scores[subreddit_name]
            
            out_data['subreddit_data'][subreddit_name]['data'] = text_scores

        with open(f'{time.time()}_{search_term}.json') as outfile:
            
            out_file.write(json.dumps(out_data,indent=4))

    print(f'"{search_term}": {final_avg_score}')