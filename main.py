import tweepy
from wordcloud_fa import WordCloudFa
from os import path
from PIL import Image
import numpy as np
import re
import json


with open('config.json', 'r') as f:
    dev = json.load(f)

dev = dev['twitter']

consKey = dev['consKey'] 
consSecret = dev['consSecret'] 
accessKey = dev['accessKey']
accessSecret = dev['accessSecret']

d = path.dirname(__file__)

auth = tweepy.OAuthHandler(consumer_key=consKey, consumer_secret=consSecret)

auth.set_access_token(accessKey, accessSecret)

api = tweepy.API(auth)

numberOfPages = 1
numberOfTweetsPerPage = 200
counter = 0
cloud = ""
txt = ""

username = input("Enter the username: ")
numberOfTweets = int(input("Enter the number of tweets: "))

if numberOfTweets > 200:
    numberOfPages = int(numberOfTweets/200)
else:
    numberOfTweetsPerPage = numberOfTweets


for i in range(numberOfPages):
    tweets = api.user_timeline(screen_name=username, count=numberOfTweetsPerPage, page=i)
    for each in tweets:
        cloud = each.text
        cloud = re.sub(r'[A-Za-z@_]*', '', cloud)
        counter += 1
        txt = txt + ' ' + each.text
        print(counter, cloud)


txt = re.sub(r'[A-Za-z@]*', '', txt)

twitter_mask = np.array(Image.open(path.join(d, "twitter-logo.jpg")))


stop = ['می', 'من', 'که', 'به', 'رو', 'از', 'ولی', 'با', 'یه', 'این', 'نمی',
        'هم', 'شد', 'ها', 'اما', 'تو', 'واقعا', 'در', 'نه', 'دارم', 'باید',
        'آره', 'برای', 'تا', 'چه', 'کنم', 'بود', 'همه', 'دیگه', 'ای', 'اون',
        'تی', 'حالا', 'بی', 'د', 'چرا', 'بابا', 'منم', 'کیه', 'توی', 'نیست', 'چی', 'باشه', 'که',
        'بودم', 'می کنم', 'که', 'اینه', 'بهتر', 'داره', 'اینه', 'که']
wc = WordCloudFa(
    persian_normalize=True,
    max_words=30000,
    margin=0,
    width=3000,
    height=2500,
    min_font_size=1,
    max_font_size=3000,
    background_color="white",
    mask=twitter_mask,
    include_numbers=False,
    stopwords=stop

).generate(txt)

image = wc.to_image()
image.show()
image.save('twitter.png')
