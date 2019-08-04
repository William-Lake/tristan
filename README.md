# tristan

*T*argeted *R*edd*I*t *S*enTiment *AN*alyzer

When given a search term/phrase and a list of subreddits, tristan gathers all the submissions in the subreddits mentioning the search term/phrase in the title and then averages the sentiment score of their titles and top comments' text.

## Libraries

Makes use of:

- nltk
- vaderSentiment
- praw

## Usage

*NOTE THAT* tristan will not work as is. See the section **Making tristan your own** for more info.

### Install

`pip install -r requirements.txt`

### Help

`python main.py -h`

```
usage: Tristan [-h] [--write_out] search_term subreddits [subreddits ...]

positional arguments:
  search_term
  subreddits

optional arguments:
  -h, --help   show this help message and exit
  --write_out
```

### Execution

`python main.py --write_out "Red Sox" baseball`

```
INFO:root:Initializing Reddit Util
INFO:root:Gathering relevant text for Red Sox
INFO:root:Initializing TextAnalyzer
INFO:root:Scoring Relevant Text
INFO:root:Calculating Average Scores
INFO:root:Writing collected data to file
"Red Sox": 0.04510824047216183
```

## Making tristan your own

tristan is currently setup to use a reddit account I put together for it. To make it your own:

1. Create a reddit account.
2. Follow reddit's quick steps for creating an app: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
3. Alter praw.ini, adding in your own account's data and name.
4. Perform a find/replace on the code base, looking for 'tristan_bot' and replacing it with the name you provided in square brackets in praw.ini.