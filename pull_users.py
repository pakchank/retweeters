import twitter_tokens
import csv
from mySQL_connector import *

conn = create_cnx()
c = create_cursor(conn)

i = 1
while True:
    c.execute("SELECT user FROM database WHERE num = {}".format(str(i)))
    
    screen_name = c[0][0]

    send_it_to Twitte here!

    if exceed limits, stop! import error from twwweee
    
    
