import tweepy
import logging
import time
import json
import urllib
import os
import safygiphy
import random
import datetime
logging.captureWarnings(True)
'''
^To suppress these warnings-
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:315: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning.SNIMissingWarning
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:120: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.InsecurePlatformWarning
'''

consumer_key = 'your_consumer_key'
consumer_secret = 'your_con_sec'
access_token = 'your_acc_tok'
access_token_secret = 'your_token'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser(), wait_on_rate_limit=False, wait_on_rate_limit_notify=False)


def get_gif_url(query):
	giphyInstance = safygiphy.Giphy()
	return random.choice(giphyInstance.search(q=query)['data'])['url']


def reply_gifs_on_mentions():
	if not os.path.isfile("latest_id_processed"):
		print "file doesnt exist, creating.."
		file("latest_id_processed", 'w').close()

	with open("latest_id_processed","rb") as last_id_keeping_file:
		readData = last_id_keeping_file.read()
		if(readData == ''):
			last_id_processed = 0
		else:
			last_id_processed = int(readData);
		last_id_keeping_file.close()



	print "Got " + str(last_id_processed) + " as ID"

	latest_id_processed = last_id_processed;


	mentionObjects = api.mentions_timeline()
	print "Last processed Id = " + str(last_id_processed) + "\n"

	for mentionObject in mentionObjects :
		currentId = int(mentionObject['id'])
		currentText = mentionObject['text']
		reply_text = get_gif_url(currentText)
		user_screen_name = mentionObject['user']['screen_name']

		print "Current Id=" + str(currentId)+", Last ProcessedId="+str(last_id_processed)
		if(currentId > last_id_processed):
			print "Processing :"
			print str(user_screen_name) +"," +str(currentId)
			print currentText
			try :
				status = "@" +str(user_screen_name) + " " + str(reply_text)
				newtObj = api.update_status(status = status, in_reply_to_status_id = currentId)
				print "newtObj reply status id is " + str(newtObj['in_reply_to_status_id'])
				print "\n"
				if(currentId>latest_id_processed):
					latest_id_processed = currentId
			except tweepy.TweepError as e:
				print "Error : " +e.message[0]['message']
				print "\n"
		else:
			print "Not Processed :"
			print str(user_screen_name) +"," +str(currentId)
			print currentText
			print "\n"
			break;

	print "Updated latest_id_processed = " + str(latest_id_processed)
	with open("latest_id_processed","w") as f:
		f.write(str(latest_id_processed))



if __name__ == '__main__':
	while (1):
		reply_gifs_on_mentions()
		print str(datetime.datetime.now()) + " : Sleeping for 120 secs.."
		time.sleep(120)	
