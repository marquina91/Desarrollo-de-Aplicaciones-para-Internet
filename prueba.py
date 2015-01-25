import tweepy
import time
# Consumer keys and access tokens, used for OAuth
consumer_key = '8WCVKxZMuLarti1uiPL71VHCX'
consumer_secret = 'aRehFSGOTdTuUaDXGgGlTVSd2SdnmRFBCneuZlHkvDhBXDkk0U'
access_token = '490393219-LTGxoqDmWciKFLBxMOaGSog2j20dSPngrQkuoMP1'
access_token_secret = 'iTyEHiqWe72GvJtD946F5PJpOJh3eUrXCo2Nl3S59a1aH'
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
# https://dev.twitter.com/docs/api/1.1/get/search/tweets

api = tweepy.API(auth)
ok='ETSIIT'
for tweets in api.search(q=ok,count=2, result_type='recent'):#geocode='37.1808605,-3.6179068,60km'
	print(tweets.created_at)
	print(tweets.user.screen_name)
	print(tweets.text)
	print(' *'*20)
	
print('/n')	
print('/n')	
print('/n')	
cuenta=0;

for tweets in api.search(q='ETSIIT', since='2015-1-2',until='2015-1-5'):#geocode='37.1808605,-3.6179068,60km'
	cuenta=cuenta+1
	
print(cuenta)

laFecha = time.localtime(time.time())
cadena=str(laFecha[0])+'-05' 
print(cadena)