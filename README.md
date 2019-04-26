# retweeters

- twitter_tokens.py: Information about twitter tokens.
- mySQL_connector.py: Build cursors to a local MySQL database where retweets are stored.

- pull_users.py: Pull retweeters from the database, look up `retweeters.csv`, and send it to Barberas code.  
- eval_ideo.R: Receive user name from `pull_users.py` and evaluate ideology. Need Twitter tokens here. 

- retweeters.csv: Store screen names of reweeters who are already evaluated.
