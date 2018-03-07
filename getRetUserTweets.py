
import twitter
import configparser as ConfigParser
import pandas as pd
from pathlib import Path
import csv
import pickle



def auto_getUserTimeLine(api, screen_name, max_count, since_id):
	statuses = api.GetUserTimeline(screen_name=screen_name, max_id=since_id, count = max_count)
	return statuses

def job():
	cp = config('test.conf')
	pickelFileName = "retweeted.pickle"
	userToIndex = "userToIndex.pickle"
	storeData(userToIndex, {})
	consumer_key, consumer_secret, access_token, access_token_secret = getAuthConfig(cp, "auth")
	api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
	getUserConfig(api, pickelFileName, None, 200, userToIndex)	 

	# statuses = auto_getUserTimeLine(api, screen_name, 100, since_id)

def getUserConfig(api, pickelFileName, since_id, max_count, userToIndex):
	dict = loadData(pickelFileName)
	fields = ['screen_name', 'text', 'isRetweeted']
	with open('userText.csv', 'w') as csvfile:
		csvwriter = csv.writer(csvfile,  delimiter=',')
		csvwriter.writerow(['screen_name', 'text', 'isRetweeted'])
		for key in dict.keys():
			statuses = auto_getUserTimeLine(api, key, max_count, since_id)
			for status in statuses:
				screen_name = key
				screen_name = translateToIndex(screen_name, userToIndex)
				text = status.text
				isRetweeted = 0
				if dict[key] == status.id:
					isRetweeted = 1
				csvwriter.writerow([screen_name, text, isRetweeted])

def translateToIndex(screen_name, userToIndex):
	dict = loadData(userToIndex)
	if screen_name in dict.keys():
		return dict[screen_name]
	else:
		dict[screen_name] = len(dict.keys()) + 1
	storeData(userToIndex, dict)

# def writeCSVFile(statuses, writeFileName):
# 	# write content to csv file.
# 	since_id_content = []
# 	text_content = []
# 	retweeted_id = []
# 	my_file = Path("/writeFileName")
# 	if my_file.exists():
# 		df = pd.read_csv(csv_file)
# 		retweeted_id = df.retweeted_id
# 		since_id_content = df.since_id_content
# 		text_content = df.text_content


# 	if statuses:
# 		for status in statuses:
# 			since_id_content.append(status.id)
# 			text_content.append(processString(status.text))
# 			if status.retweeted_status:
# 				retweeted_id.append(status.retweeted_status.id)
# 			else:
# 				# 18 digits 0 indicating not retweeted
# 				retweeted_id.append(000000000000000000)

# 	# dataframe = pd.DataFrame({'retweeted_id':retweeted_id, 'since_id':since_id_content,'text':text_content})
# 	# dataframe.to_csv(writeFileName, index=False, sep=',')



def loadData(pickelFileName):
	with open(pickelFileName, 'rb') as handle:
		unserialized_data = pickle.load(handle)
	return unserialized_data

def storeData(pickelFileName, dict):
	with open(pickelFileName, 'wb') as handle:
		pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def config(configFile):
	cp = ConfigParser.SafeConfigParser()
	cp.read(configFile)
	return cp

def getAuthConfig(cp, auth):
	consumer_key = cp.get(auth, 'consumer_key')
	consumer_secret = cp.get(auth, 'consumer_secret')
	access_token = cp.get(auth, 'access_token')
	access_token_secret = cp.get(auth, 'access_token_secret')
	return consumer_key, consumer_secret, access_token, access_token_secret


def main():
	job()


if __name__ == "__main__":
    main()








