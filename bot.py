# import sys
import twitter
import configparser as ConfigParser
import pandas as pd

def auto_tweets(api, msg):
	message = msg
	status = api.PostUpdate(message)
	
def auto_getUserTimeLine(api, screen_name, max_count):
	user = screen_name
	statuses = api.GetUserTimeline(screen_name=screen_name, count = max_count)
	return statuses

def auto_favorite_auto_tweet(api, posted_tweets):
    for status in posted_tweets:
        if status.favorited == False:
            api.CreateFavorite(status_id=status.id)
        if status.retweeted == False:
            api.PostRetweet(status_id=status.id)

# In case detected automated activity, do not use it.
def auto_reply(api, statuses, screen_name, msg):
	for sts in statuses:
		api.PostUpdate(status="@"+ screen_name + " "+ msg, in_reply_to_status_id=sts.id)

def main():
	cp = ConfigParser.SafeConfigParser()
	cp.read('test.conf')
	# Later add checks here, in case test.conf do not have auth section.
	consumer_key = cp.get('auth', 'consumer_key')
	consumer_secret = cp.get('auth', 'consumer_secret')
	access_token = cp.get('auth', 'access_token')
	access_token_secret = cp.get('auth', 'access_token_secret')

	api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
	screen_name = cp.get('user', 'screen_name')
	statuses = auto_getUserTimeLine(api, screen_name, 10)
	print(len(statuses))
	
	# new_since_id = "970073708357337089"
	# cp.set('user', 'since_id', new_since_id)
	# cp.write(open('test.conf', 'w'))  
	# auto_reply(api, statuses, screen_name, msg)
	# auto_favorite_auto_tweet(api, statuses)
	for status in statuses:
		print(status)

	# writeFileName = 'status1.csv'
	# since_id_content = []
	# text_content = []
	# if statuses:
	# 	with open('userPipeline.json', 'a') as f:
	# 		for status in statuses:
				
	# 			f.write(str(status))

	# 			since_id_content.append(status.id)
	# 			text = status.text.replace(',', ' ')
	# 			text = status.text.replace('\n', ' ')
	# 			text_content.append(text)
	# 		# text_content.append(status.text)
	# dataframe = pd.DataFrame({'since_id':since_id_content,'text':text_content})
	# dataframe.to_csv(writeFileName, index=False, sep=',')



if __name__ == "__main__":
    main()



