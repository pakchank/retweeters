import twitter_tokens
import csv
import time
import subprocess
from mySQL_connector import *

conn = create_cnx()
c = create_cursor(conn)

i = 0
while True:
    i += 15
    c.execute("SELECT user FROM database WHERE num >=  {} AND num <= {}".format(str(i-14), str(i)))
         
    screen_names = [row[0] for row in c]

    with open("retweeter.csv") as f:
        retweeters = f.csv_write()

    # Look up retweeter.csv here

    screen_names = [retweeter in retweeter for screen_names if retweeter not in retweeters]

    # Get ideology from R code.  
    subprocess.call("Rscript --vanilla eval_ideo.R {}".format("("+screen_name+")". shell=True)

    # Append new retweeters -> maybe add it as JSON (with ideology info)
    retweeters.append(screen_names)
    with open("reteeter.csv") as f:
       # Append here (not above)
 
    time.sleep(15 * 60)
       
    #if exceed limits, stop! import error from twwweee
    
c.disconnect()
