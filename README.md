# retweeters
This project pull retweets from Twitter Streaming API, and feed the retweeters' information to Twitter Search API to evaluate their ideology.

# 1. Scraping Retweets
- `scraper.py`: Scrape retweets from Twitter Streaming API
- `private.py`: (Private setting) Twitter API credential for scraping
- `settings.py`: (Private setting) Database setting

# 2. Evaluating Retweeters
- twitter_tokens.py: (Private setting) Information about twitter tokens.
- mySQL_connector.py: (Private setting) Build cursors to a local MySQL database where retweets are stored.

- pull_users.py: Pull retweeters from the database, look up `retweeters.csv, and send it to Barberas code.  
- eval_ideo.R: Receive user name from `pull_users.py` and evaluate ideology. Need Twitter tokens here. 

- retweeters.csv: Store screen names of reweeters who are already evaluated.
