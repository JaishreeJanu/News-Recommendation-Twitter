import sys
import csv

#http://www.tweepy.org/
import tweepy

#Get your Twitter API credentials and enter them here


consumer_key = 'UtXVnKCvSe2CL6uHfKjTkwFIC'
consumer_secret = 'uRAHe9Fj0bp5FKUFWc95hTLYSCsgKfynshkET0fRPixL0dCXmA'
access_token = '925610881588875264-jSGe9srWUVrue8u9BOVJeiwQSDJZatR'
access_secret = '2sXaXcTh2ZE9PMUwDYluhhGvPFowVcpt209p3raWOO7l7'

#method to get a user's last 100 tweets
def get_tweets(username):

	#http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	#set count to however many tweets you want; twitter only allows 200 at once
	number_of_tweets = 100

	#get tweets
	tweets = api.user_timeline(screen_name = username,count = number_of_tweets)

	#create array of tweet information: username, tweet id, date/time, text
	tweets_for_csv = [[username,tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]

	#write to a new csv file from the array of tweets
	print "writing to {0}_tweets.csv".format(username)
	with open("{0}_tweets.csv".format(username) , 'w+') as file:
		writer = csv.writer(file, delimiter='|')
		writer.writerows(tweets_for_csv)


#if we're running this as a script
if __name__ == '__main__':

    #get tweets for username passed at command line


    #alternative method: loop through multiple users
	users = ['THexplains','timesofindia']

	for user in users:
		get_tweets(user)
