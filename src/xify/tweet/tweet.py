import json
import logging

logger = logging.getLogger(__name__)

# this will create a tweet, with possiblities of adding medias and replying to other tweets
def create_tweet(tas, message, media_ids = None, reply_ids = None):
	logger.info(f"""Attempting to send tweet with the message:"{message}", media IDs:{media_ids} and reply IDs:{reply_ids}""")

	# double checking the formats of the media and reply ids
	if isinstance(media_ids, str):
		media_ids = [media_ids]
	
	if isinstance(reply_ids, str):
		reply_ids = [reply_ids]
		
	payload = {"text": message}
	
	if media_ids != None:
		payload["media"] = {
			"media_ids":media_ids
		}
		
	if reply_ids != None:
		payload["reply"] = {
			"in_reply_to_tweet_id":reply_ids
		}
	
	headers = {
		"content-type":"application/json"
	}
	r = tas.post("https://api.twitter.com/2/tweets", data = json.dumps(payload), headers = headers)
	resp = json.loads(r.text)

	if 200 <= r.status_code <= 299:
		tweet_id = resp["data"]["id"]

		logger.info(f"Tweet has been successfully sent! ID: {tweet_id}")

		return tweet_id
	
	else:
		logger.critical(f"Tweet could not be sent! Reason: {r.status_code} | {r.text}")

# this will delete a tweet based on a given tweet-id
def delete_tweet(tas, tweet_id):
	r = tas.delete(f"https://api.twitter.com/2/tweets/{tweet_id}")
	resp = json.loads(r.text)

	if resp["data"]["deleted"]:
		logger.info("Tweet has been successfully deleted!")

	else:
		logger.critical(f"Tweet could not been deleted! Reason: {r.status_code} | {r.text}")
