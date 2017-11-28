import tweepy
import time
import csv
import os

consumer_key = "EoZiw1Po4vykdZgMjo2zIVgoH"
consumer_secret = "imHVLRZAl6Xu71KfpG8OFU6px5vHBIM4EqzF4ijBJr4fL8VHc9"
access_key = "915591987738312705-DBeC5LQnBepkH9XQqTwrZfxW35ZjEsR"
access_secret = "kNr9QUJrN3MryJ4klz7XxWC4zpQfk6dEXd8cj2nLPTfbw"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_uniqueId(screen_name):
    try:
        user_profile = api.get_user(screen_name)
        id = user_profile.id_str
    except:
        id = "broken"
    
    return id

def get_tweets(screen_name):
    alltweets = []
    try:
        # for tweets in tweepy.Cursor(api.user_timeline, id=screen_name).items():
        #     alltweets.extend(tweets)
        # alltweets = tweepy.Cursor(api.user_timeline, id=screen_name).items()
        #https://developer.twitter.com/en/docs/tweets/timelines/overview describes user_timeline
        tweets = api.user_timeline(screen_name, count=200)
        # print "tweets"
        alltweets.extend(tweets)
        oldest = alltweets[-1].id - 1
        # print oldest
        # print len(tweets)
        while len(tweets) > 0:
            tweets = api.user_timeline(screen_name, count=200, max_id=oldest)
            alltweets.extend(tweets)
            oldest = alltweets[-1].id - 1
    except:
        user_profile = "broken"
    return alltweets

def get_max_retweet_count(tweets):
    list1 = []
    text1 = ""
    for tweet in tweets:
        list1.append(tweet.retweet_count)
#     return max(list1)
# def get_most_popular_tweet(tweets, max_retweet_count):
    for tweet in tweets:
        if tweet.retweet_count == max(list1):
            text1 = tweet.text
    return (text1,max(list1))

def save_csv(tweets, text, filename):
    count = 0
    with open (filename, 'wb') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["id","user","created_at","text"])
        for tweet in tweets:
            if text in tweet.text:
                count+=1
                writer.writerow([tweet.id_str,tweet.user.screen_name,tweet.created_at,tweet.text.encode('unicode-escape')])
    return count

username = raw_input("\nEnter the Twitter username for which Unique Id is needed\n")
# print username
# # uid = get_uniqueId(username)
print "Answer for Q1: The Id for " +username+ " is " +str(get_uniqueId(username))
citrontweeets = get_tweets("CitronResearch")
text2, max_list = get_max_retweet_count(citrontweeets)
print "Answer for Q2: The most popular tweet of citron research is: \"" + text2 + " \" with a retweet count of " +str(max_list)
shopifytweets = get_tweets("Shopify")
no_of_shopify_tweets= save_csv(shopifytweets, "citron", 'shopify.csv')
print "Answer for Q3: The total number of tweets which mentions citron in shopify official account are " +str(no_of_shopify_tweets)+ " and they have been saved in shopify.csv"

tobitweets = get_tweets("tobi")
no_of_tobi_tweets= save_csv(tobitweets, "short-selling troll", 'tobi.csv')
print "Alternative answer for Q3: The total number of tweets which mentions citron as a short-selling troll in Tobi Lutke official account are " +str(no_of_tobi_tweets)+ " and they have been saved in tobi.csv"


no_of_citron_tweets= save_csv(citrontweeets, "FTC", 'Citron.csv')
print "Answer for Q4: The total number of tweets which mentions FTC in citron official account are " +str(no_of_citron_tweets)+ " and they have been saved in citron.csv"

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
print "Answer for Q5: All the tweets obtained above have been successfully saved in the path " +path+ " as csv files" 
# for tweets in tweepy.Cursor(api.user_timeline, id="CitronResearch").items():
#     print tweets.text

# text2 = get_most_popular_tweet(t, max_list)
