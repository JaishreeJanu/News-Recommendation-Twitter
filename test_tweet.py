from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
 
consumer_key = 'UtXVnKCvSe2CL6uHfKjTkwFIC'
consumer_secret = 'uRAHe9Fj0bp5FKUFWc95hTLYSCsgKfynshkET0fRPixL0dCXmA'
access_token = '925610881588875264-jSGe9srWUVrue8u9BOVJeiwQSDJZatR'
access_secret = '2sXaXcTh2ZE9PMUwDYluhhGvPFowVcpt209p3raWOO7l7'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#anushkaSharma'])
twitter_stream.filter(track=['#delhi gov'])
twitter_stream.filter(track=['#T20'])
twitter_stream.filter(track=['#computer technology'])
twitter_stream.filter(track=['#ekdilekjaan'])
