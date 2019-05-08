#import twitter_tokens
import csv
import time
import subprocess
import asyncio 
from mySQL_connector import *
from pathlib import Path

# Need to comment out the following three lines when re-run this code.
with open('retweeter_ideo.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["user","mean_ideo"])    # Needs to have more rows.

conn = create_cnx()
c = create_cursor(conn)

i = 0
# Below should be changed --> Only the first column
retweeter_list = Path("retweeter.csv")

async def get_ideo_score(API_key):
    global i 
    while True:
        i += 1
        print(i)
    
        c.execute("SELECT user_name FROM xudong WHERE num = {}".format(str(i)))
        
        # If there's no retweets in db, stop.
        if c == None:
            break
        
        screen_names = [row[0] for row in c]
    
        if retweeter_list.is_file():
            with open(retweeter_list, mode='r') as f: 
                retweeters = [row.split()[0] for row in f]
        else:
            retweeters = list()

        screen_names = [retweeter for retweeter in  screen_names if retweeter not in retweeters]

        print("Retrieving ideology scores of :" + ", ".join(screen_names))
    
        # Get ideology from R code.  
        print("Rscript --vanilla eval_ideo.R {} {}".format(" ".join(screen_names), API_key))
        subprocess.call("Rscript --vanilla eval_ideo.R {} {}".format(" ".join(screen_names), API_key), 
                shell=True)

loop = asyncio.get_event_loop()

task1 = loop.create_task(get_ideo_score("KEY_1"))
task2 = loop.create_task(get_ideo_score("KEY_2"))
task3 = loop.create_task(get_ideo_score("KEY_3"))

loop.run_until_complete(asyncio.gather(task1, task2, task3))
   
c.close()
conn.close()
