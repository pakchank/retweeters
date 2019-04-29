#import twitter_tokens
import csv
import time
import subprocess
from mySQL_connector import *
from pathlib import Path

conn = create_cnx()
c = create_cursor(conn)

i = 0
while True:
    i += 15
    c.execute("SELECT user_name FROM xudong LIMIT 15")
    #c.execute("SELECT user FROM database WHERE num >=  {} AND num <= {}".format(str(i-14), str(i)))
         
    screen_names = [row[0] for row in c]

    retweeter_list = Path("retweeter.csv")
    
    if retweeter_list.is_file():
        with open(retweeter_list, mode='r') as f: 
            retweeters = [row.split()[0] for row in f]
    else:
        retweeters = list()

    # Look up retweeter.csv here

    screen_names = [retweeter for retweeter in  screen_names if retweeter not in retweeters]

    # Get ideology from R code.  
    print("Rscript --vanilla eval_ideo.R {}".format(" ".join(screen_names)))
    subprocess.call("Rscript --vanilla eval_ideo.R {}".format(" ".join(screen_names)), shell=True)
    # Should be something like "x = subprocess.check_output(cmd, universal_newlines=True)
    
    ## Then, how do I get the results? as dic {"users_name": "score", ...}
    
    #dict_score = dict()
    #for user, score in some_results.items():
    #    dict_score[user] = score

    #with open("reteeter.csv", mode='a') as f:
    #    for user, score in dict_score.items():
    #        f.write(user, score)

    print(screen_names)

    time.sleep(15 * 60)
       
    #if exceed limits, stop! import error from twwweee
    
c.close()
conn.close()
