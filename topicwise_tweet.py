from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import preprocessor as pp

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'HM0jiaMXJyiterDuooBg7inf6'
consumer_secret = 'RHdftTy18PUUf5lnUF6IEMwxXn6U0eTc8R10FbTFhAQ2wQ1lor'
access_token = '930308807317774336-geNWlSFQL7pklYJwlHFaEb0S8ezoOBF'
access_secret = 'h91eSHipaSxmjFhb8DDcTC3vHklnRb2WLYuxUbiPMTQKW'




#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data
         f = open("tweets_text.csv","a")
         writer = csv.writer(f, delimiter='|')
         b = pp.clean(data)
         res = json.loads(b)
         a = [res['text']]
         print(a)
         
         return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    print"fg"
   
   
    stream.filter(track=['#ChildrensDay','#TuesdayThoughts','#WorldDiabetesDay','#PledgeAgainstPollution','#DriversOfTomorrow','Chacha Nehru','Italy','Prime Minister'])
    

  
