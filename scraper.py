import settings
import tweepy
import dataset
#from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
from mySQL_connector import *
import json
import time
import math

#conn = create_cnx()
#c = create_cursor(conn)

#c.execute("ALTER DATABASE twitter CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci")
#c.execute("DROP TABLE IF EXISTS {}".format(settings.TABLE_NAME))
#c.execute('''CREATE TABLE IF NOT EXISTS {}
#            (description text, loc text, texts text, coords text, geo text, name text,
#            user_created text, followers text, id_str text, 
#            created text, retweets text, bg_color text)'''.format(settings.TABLE_NAME))
#c.execute("ALTER TABLE {} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(settings.TABLE_NAME))
#c.execute('''ALTER TABLE {} MODIFY COLUMN texts text
#        CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL'''.format(settings.TABLE_NAME))
#c.execute("SET NAMES utf8mb4")

#c.close()
#conn.close()

db = dataset.connect(settings.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.siesta = 0
        self.nightnight = 0

    def on_status(self, status):
        if status.retweeted:
            return
        
        if status.user.description:
            description = status.user.description.encode("ascii","ignore").decode("utf-8","ignore")
        else:
            description = ""
       
        if status.user.location:
            loc = status.user.location.encode("ascii","ignore").decode("utf-8","ignore")
        else:
            loc = ""

        if status.text:
            text = status.text.encode("ascii","ignore").decode("utf-8","ignore")
        else:
            text = ""
        
        coords = status.coordinates
        geo = status.geo
        
        if status.user.screen_name:
            name = status.user.screen_name.encode("ascii","ignore").decode("utf-8","ignore")
        else:
            name = ""
        
        user_created = status.user.created_at
        followers = status.user.followers_count
        if status.id_str:
            id_str = status.id_str.encode("ascii","ignore").decode("utf-8","ignore")
        else:
            id_str = ""

        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        #blob = TextBlob(text)
        #sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[settings.TABLE_NAME]  ## Change HERE!!!

        try:
            tweet_dict = dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                texts=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color)
                #,
                #polarity=sent.polarity,
                #subjectivity=sent.subjectivity)
            table.insert(tweet_dict)
        
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + str(sleepy/60) + " minutes.")
            time.sleep(sleepy)
            slef.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt wiil occur in " + str(sleepy) + " seconds.")
            time.sleep(sleepy)
            self.nightnight += 1
        return True
            

auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)

