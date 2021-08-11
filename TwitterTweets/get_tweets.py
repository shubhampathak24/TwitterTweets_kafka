import tweepy
import pandas
import json # The API returns JSON formatted text

access_token = "Get your own"
access_token_secret =  "Get your own"
consumer_key =  "Get your own"
consumer_secret =  "Get your own"

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

TRACKING_KEYWORDS = ['covid']
OUTPUT_FILE = "tweets.txt"
TWEETS_TO_CAPTURE = 5000

class MyStreamListener(tweepy.StreamListener):
    """
    Twitter listener, collects streaming tweets and output to a file
    """
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open(OUTPUT_FILE, "w")

    def on_status(self, status):
        tweet = status._json
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        
        # Stops streaming when it reaches the limit
        if self.num_tweets <= TWEETS_TO_CAPTURE:
            if self.num_tweets % 100 == 0: # just to see some progress...
                print('Numer of tweets captured so far: {}'.format(self.num_tweets))
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)

#%%time #let's see how long it takes

# Initialize Stream listener
l = MyStreamListener()

# Create you Stream object with authentication
stream = tweepy.Stream(auth, l)

# Filter Twitter Streams to capture data by the keywords:
stream.filter(track=TRACKING_KEYWORDS)

import matplotlib.pyplot as plt
# Initialize empty list to store tweets
tweets_data = []
OUTPUT_FILE = "tweets.txt"
# Open connection to file
with open(OUTPUT_FILE, "r") as tweets_file:
    # Read in tweets and store in list
    for line in tweets_file:
        tweet = json.loads(line)
        tweets_data.append(tweet)

df = pandas.DataFrame(tweets_data, columns=['created_at','lang', 'text', 'source'])
# Just convert to datetime
df['created_at'] = pandas.to_datetime(df.created_at)
# Regular expression to get only what's between HTML tags: > <
df['source'] = df['source'].str.extract('>(.+?)<', expand=False).str.strip()
print(df.head())

html = df.to_html()

#write html to file
text_file = open("index.html", "w",encoding='utf-8')
text_file.write(html)
text_file.close()

# create filter for most popular languages
lang_mask = (df.lang == 'en') | (df.lang == 'ca') | (df.lang == 'fr') | (df.lang == 'es')

# create a filter for most popular sources
source_mask = (df.source == 'Twitter for iPhone') | (df.source == 'Twitter for Android')\
    | (df.source == 'Twitter Web Client') | (df.source == 'Twitter for iPad') \
    | (df.source == 'Twitter Lite') | (df.source == 'Tweet Old Post')


(df[lang_mask & source_mask].groupby(['source','lang']) # apply filter/groupby
 .size() # get count of tweets per source/lang
 .unstack() # unstack to create new DF 
 .fillna(0) # fill NaN with 0
 .plot(kind='bar', figsize=(14,7), title='Tweets by source and language') # plot
)

#df.plot( kind = 'bar')
plt.savefig('pic.png')
plt.show()