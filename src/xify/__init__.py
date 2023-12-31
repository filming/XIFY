import sys
import os
import logging

from .auth.tas import create_tas
from .tweet.tweet import create_tweet, delete_tweet
from .tweet.media import get_media_id, format_media_ids

STORAGE_DIR_PATH = "../storage"
LOGS_DIR_PATH = f"{STORAGE_DIR_PATH}/logs"

if not os.path.exists(STORAGE_DIR_PATH): os.mkdir(STORAGE_DIR_PATH)
if not os.path.exists(LOGS_DIR_PATH): os.mkdir(LOGS_DIR_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"{LOGS_DIR_PATH}/xify.log", "w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

class XIFY:
    def __init__(self):
        self.tas = None
        self.auth_uid = 0
        self.auth_username = ""

        logger.info("An instance of XIFY has been created.")

    # create twitter authorized session object
    def create_tas(self):
        logger.info("Attempting to authorize XIFY instance with API keys.")

        self.tas, self.auth_uid, self.auth_username = create_tas()
        
    # takes a file, uploads it to twitter and returns a media id to access the file media
    def get_media_id(self, filepath):
        logger.info(f"Attempting to get media ID for the file located at '{filepath}'.")

        media_id = get_media_id(self.tas, filepath)

        return media_id
    
    # takes a list of media ids and break it into groups of 4 if possible
    def format_media_ids(self, media_ids):
        logger.info(f"Attempting to format a list of {len(media_ids)} media IDs.")

        media_id_sections = format_media_ids(media_ids)

        return media_id_sections
    
    # this will create a tweet, with possiblities of adding medias and replying to other tweets
    def create_tweet(self, message = "", media_ids = None, reply_ids = None):
        logger.info("Attempting to send a tweet.")

        tweet_id = create_tweet(self.tas, message, media_ids, reply_ids)

        return tweet_id
    
    # this will delete a tweet based on a given tweet-id
    def delete_tweet(self, tweet_id):
        logger.info(f"Attempting to delete a tweet with ID: {tweet_id}.")

        delete_tweet(self.tas, tweet_id)
