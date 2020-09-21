# tristan

*T*argeted *R*edd*I*t *S*enTiment *AN*alyzer

A Bottle REST Api for searching across Subreddits for some text and calculating an average sentiment from the results.

When given a search term/phrase and a list of subreddits, tristan gathers all the submissions in the subreddits mentioning the search term/phrase in the title and then averages the sentiment score of their titles and top comments' text.

## Libraries

Makes use of:

- nltk
- TextBlob
- praw

## Usage

*NOTE THAT* tristan will not work as is. See the section **Making tristan your own** for more info.

### Install

`pip install -r requirements.txt`

### Startup

`cd /path/to/tristan/dir`

_Basic_

`python tristan`

_Specifying the port_

`python tristan --port 8676`

_Output when ready_

```
INFO:root:Initializing Reddit Util
Bottle v0.12.17 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:9010/
Hit Ctrl-C to quit.
```

### Calling Tristan

There's only one endpoint `/tristan` which excepts POST requests with a json body containing a list of queries. Each query is formatted like so:

```json
    {
      "subreddits": [
        "AListOfSubredditNames",
        "ToUseWhenSearchingForYourText"
      ],
      "search_text":"The text to search the subreddits for."
    }
```

Each query is provided as one element in a json array whose key value in the global Json object is "queries":

```json
{
  "queries":[
    {
      "subreddits": [
        "NameofSubredditToSearchForInTheFirstQuery",
        "ToUseWhenSearchingForYourText"
      ],
      "search_text":"This is the text to search for in the first query."
    },
    {
      "subreddits": [
        "NameofSubredditToSearchForInTheSecondQuery",
        "AnotherSubredditName"
      ],
      "search_text":"This is the text to search for in the second query."
    }
  ]
}
```

The returned content is a Json Array. Each entry in the array is a json object formatted like so:

```json
    {
        "query": { 
          "subreddits": [
            "AListOfSubredditNames",
            "AnotherSubredditName"
          ],
          "search_text":"This is the text to search for in the second query."
        },
        "avg_score": -0.075,
        "avg_scores": {
            "AListOfSubredditNames": 0.15,
            "AnotherSubredditName": -0.3 
        },
        "subreddit_data": {
            "AListOfSubredditNames": {
                "avg_score": 0.15,
                "data": {
                    "First Sentence": 0.1,
                    "Second Sentence": 0.2
                }
            },
            "AnotherSubredditName": {
                "avg_score": 0.05,
                "data": {
                    "First Sentence": -0.3,
                    "Second Sentence": 0.4
                }
            }
        }
    }
```

Where:

- `query` is the original query that the results are for,
- `avg_score` is the average score of the final subreddit searches,
- `avg_scores` is the breakdown of average scores across the subreddits, and
- `subreddit_data` is the breakdown of the individual scores in each subreddit.

So for example:

```json
{
  "queries":[
    {
      "subreddits":[
        "MontanaPolitics",
        "politics"
      ],
      "search_text":"Bullock"
    },
    {
      "subreddits":[
        "MontanaPolitics",
        "politics"
      ],
      "search_text":"Daines"
    }
  ]
}
```

When used like so with curl:

`curl -d '{"queries":[{"subreddits":["MontanaPolitics","politics"],"search_text":"Bullock"},{"subreddits":["MontanaPolitics","politics"],"search_text":"Daines"}]}' -H "Content-Type: application/json" -X POST http://localhost:9010/tristan`

Returns:

```json
[
    {
        "query": {
            "subreddits": [
                "MontanaPolitics",
                "politics"
            ],
            "search_text": "Bullock"
        },
        "avg_score": 0.0954785704264871,
        "avg_scores": {
            "MontanaPolitics": 0.1286844135802469,
            "politics": 0.06227272727272728
        },
        "subreddit_data": {
            "MontanaPolitics": {
                "avg_score": 0.1286844135802469,
                "data": {
                    "The Montana Passenger Rail Summit is at 10 am on September 17! With remarks from Governor Steve Bullock, Sens. Steve Daines & Jon Tester, and Rep. Greg Gianforte. Learn more about restoring passenger rail service to southern Montana!": 0.0625,
                    "I honestly want this an incredible amount. It would be fantastic to be able to just jump on a train and head to Billings, Missoula, Helena, etc!": 0.63125,
                    "I dream of them using the southbound tracks in Missoula to make a commuter train down to Hamilton (from downtown), would be a great way to minimize the danger of traveling down that highway in the winter. And alleviating some traffic within Missoula.\n\nWould be way too expensive unfortunately I believe.": -0.11234567901234567,
                    "Would it be neat? Yeah...  Its never gonna happen. Its a waste if money talking about it, they know that..": -0.06666666666666667
                }
            },
            "politics": {
                "avg_score": 0.06227272727272728,
                "data": {
                    "Bullock unveils report on economic impact of Medicaid expansion": 0.2,
                    "\nRegister to vote or check your registration status **[here](https://www.vote.gov/)**. Plan your vote: **[Early voting](https://www.ncsl.org/research/elections-and-campaigns/early-voting-in-state-elections.aspx)** | **[Mail in voting](https://www.npr.org/2020/09/14/909338758/map-mail-in-voting-rules-by-state)**.\n\n---\n\nAs a reminder, this subreddit [is for civil discussion.](/r/politics/wiki/index#wiki_be_civil)\n\nIn general, be courteous to others. Debate/discuss/argue the merits of ideas, don't attack people. Personal insults, shill or troll accusations, hate speech, **any** advocating or wishing death/physical harm, and other rule violations can result in a permanent ban. \n\nIf you see comments in violation of our rules, please report them.\n\n For those who have questions regarding any media outlets being posted on this subreddit, please click [here](https://www.reddit.com/r/politics/wiki/approveddomainslist) to review our details as to our approved domains list and outlet criteria.\n\n***\n\n\n*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/politics) if you have any questions or concerns.*": 0.0196969696969697,
                    "> The program also brings in roughly $600 million to Montana annually, has added about 5,900 to 7,500 jobs and has created about $350 million to $385 million in personal income. These figures show that the economic benefit of expansion has been greater than the cost to the state, according to the report, which was released by the Departments of Revenue, Labor and Industry and Health and Human Services.": 0.09166666666666665,
                    "This is what Democrats do. We need Bullock in the Senate.": 0.0,
                    "Donate to his campaign if you can. Its a close race!": 0.0
                }
            }
        }
    },
    {
        "query": {
            "subreddits": [
                "MontanaPolitics",
                "politics"
            ],
            "search_text": "Daines"
        },
        "avg_score": 0.09337696092082058,
        "avg_scores": {
            "MontanaPolitics": 0.09337696092082058
        },
        "subreddit_data": {
            "MontanaPolitics": {
                "avg_score": 0.09337696092082058,
                "data": {
                    "Just emailed Daines to encourage him to resist filling the SCOTUS seat this year.": 0.0,
                    "Did your email include his [own quote](https://missoulian.com/opinion/letters/what-s-daines-position-on-hearings/article_d3425d85-098a-5936-9d45-f41f8166b25c.html) saying there should be no confirmation hearings during an election year?\n\nAlso: https://twitter.com/SteveDaines/status/710120781569724416": 0.3,
                    "I called his Helena office a couple of hours ago. And I'll call again. And again. Other than voting, it's about the only actionable thing I'm able to do at this point.": 0.03125,
                    "Thank you. Yeah, have to illusion that Daines will do anything other that what Trump commands him to do, but it can\u2019t hurt, right?": 0.040178571428571425,
                    "We gotta call. So many times. And then call some more.\n\nI'd be surprised if anyone's staffing the state offices, but PLEASE CALL.\n\nWashington DC: (202) 224-2651  \n\nMissoula: (406) 549-8198  \n\nHelena: (406) 443-3189  \n\nBozeman: (406) 587-3446  \n\nGreat Falls: (406) 453-0148\n\nPlease reply if there are more. I couldn't find numbers in Billings or Kalispell!?\n\n*edited to fix the stupid hyperlinks I had...*": -0.007142857142857133,
                    "https://www.daines.senate.gov/connect/email-steve": 0.0,
                    "Here's the transcript of my email, per request. It was off the cuff in a moment of passion, so please excuse the tongue in cheek pandering. Cut and paste if you want. I don't know if his office even gives a shit enough to notice:\n\n> Senator,\n\n> I'm writing this tonight absolutely gutted by the loss of Justice Ginsburg at this delicate time for democratic society. You absolutely cannot allow the senate majority to attempt to confirm-- i.e. ram though--a Trump picked justice this close to such a historic election. The people of Montana are not typical partisan stooges and I think you know your reelection chances this cycle are tenuous. This would be perceived as disingenuous at best, outright nefarious at worst to the majority of your constituents. \n\n> You must absolutely be one of at least 3 GOP senators to oppose any attempt to install a SCJ this year. You were party to the obstruction of Merrick Garland, who notably was nominated in March of 2016. Surely the senator would be consistent in this principle and not consent to an appointment of any SCJ this much closer to a presidential election. \n\n> You did make a token effort to stop destructive USPS reforms, which I applaud. I hope that the senator can show the same integrity in resisting any attempt to pile drive an ultra conservative justice into SCOTUS at this time. \n\n> It will break this country. I guess if that's what you want and intend, this letter is in vain. \n\n> These are dark days, Senator. Have the courage to be a beacon of light if you are able to have it in you.\n\n> God bless,\n\n> _Firstname Lastname_\n_Town_": 0.03472222222222223,
                    "Can you include his email here for us to easily cut and paste? EDIT: daines.senate.gov": 0.21666666666666667,
                    "I'm already blacklisted by his office. All they'll do is send their propaganda my way like I'm some kind of fucking moron. We're dealing with fascists and they don't care about honesty, justice, truth, integrity, or any such virtue. If it makes you feel good to know you tried though, you have that.": 0.15,
                    "It's easy to write to congress through resistbot on Twitter.": 0.43333333333333335,
                    "I called DC and Bozeman. Not expecting much from the traitorous hypocrite though.": 0.1,
                    "Thanks for this. I just did the same. We're gutted, but this did help a bit.": 0.06666666666666667,
                    "My feelings for the current president aside, I really dislike the practice of people stonewalling and bringing our judicial system to a halt. I believe that the president that is currently in power should be allowed to make appointments regardless of election years.": 0.05,
                    "Obama nominated in an election year why shouldn't Trump?": 0.0,
                    "Just emailed Daines to support him putting President Donald J. Trump's extremely qualified nominee on the SCOTUS seat!": -0.15625,
                    "The Montana Passenger Rail Summit is at 10 am on September 17! With remarks from Governor Steve Bullock, Sens. Steve Daines & Jon Tester, and Rep. Greg Gianforte. Learn more about restoring passenger rail service to southern Montana!": 0.0625,
                    "I honestly want this an incredible amount. It would be fantastic to be able to just jump on a train and head to Billings, Missoula, Helena, etc!": 0.63125,
                    "I dream of them using the southbound tracks in Missoula to make a commuter train down to Hamilton (from downtown), would be a great way to minimize the danger of traveling down that highway in the winter. And alleviating some traffic within Missoula.\n\nWould be way too expensive unfortunately I believe.": -0.11234567901234567,
                    "Would it be neat? Yeah...  Its never gonna happen. Its a waste if money talking about it, they know that..": -0.06666666666666667
                }
            },
            "politics": {
                "avg_score": "No Scores!",
                "data": {}
            }
        }
    }
]
```

## Making tristan your own

To make tristan your own:

1. Create a reddit account.
2. Follow reddit's quick steps for creating an app: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
3. Alter praw.ini, adding in your own account's data and name.
4. Perform a find/replace on the code base, looking for 'tristan_bot' and replacing it with the name you provided in square brackets in praw.ini.