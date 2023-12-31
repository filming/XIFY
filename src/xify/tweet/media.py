import os
import logging
import json
import time
import math
import time

logger = logging.getLogger(__name__)
MAX_BYTES_PER_SEG = 5000000

# takes in a list of media ids and break it into groups of 4 if possible.
def format_media_ids(media_ids):
	sections = []

	while len(media_ids) > 0:
		part = media_ids[:4]
		sections.append(part)
		media_ids = media_ids[4:]

	logger.info(f"Media IDs have been succesfully formatted into {len(sections)} sections!")

	return sections

# takes a file and returns the corresponding media attribute (MIME type)
def get_media_attributes(file_path):
	file_path_parts = file_path.split(".")

	if file_path_parts[len(file_path_parts)-1] == "png":
		return "tweet_image", "image/png"
	
	elif file_path_parts[len(file_path_parts)-1] == "jpeg":
		return "tweet_image", "image/jpeg"
	
	elif file_path_parts[len(file_path_parts)-1] == "gif":
		return "tweet_gif", "image/gif"

	else:
		return "tweet_video", "video/mp4"

# The INIT command request is used to initiate a file upload session. It returns a media_id.
def upload_init(tas, file_path):
	logger.info("Upload INIT has started.")

	media_id = ""

	payload = {
		"command":"INIT",
		"total_bytes":os.path.getsize(file_path),
		"media_type":get_media_attributes(file_path)
	}

	r = tas.post("https://upload.twitter.com/1.1/media/upload.json", data = payload)

	if 200 <= r.status_code <= 299:
		resp = json.loads(r.text)

		media_id = resp["media_id_string"]
		
		logger.info(f"Upload INIT succeeded. Media ID: {media_id}")

	else:
		logger.critical(f"Upload INIT failed. Reason: {r.status_code} | {r.text}")
	
	return media_id

# The APPEND command is used to upload a chunk (consecutive byte range) of the media file. 
# For example, a 3 MB file could be split into 3 chunks of size 1 MB, and uploaded using 3 APPEND command requests.
def upload_append(tas, file_path, media_id):
	logger.info("Upload APPEND has started.")

	payload = {
		"command":"APPEND", 
		"media_id":media_id, 
		"segment_index":-1 # setting this to -1 so we can increment at the start of the while loop instead of at the end
	} 
	
	with open(file_path, "rb") as f:
		file_content = f.read()
	
	remaining_bytes = len(file_content)
	total_segments = math.ceil(remaining_bytes / MAX_BYTES_PER_SEG)

	logger.info(f"The file located at '{file_path}' has been broken into {total_segments} segment(s).")

	while remaining_bytes > 0:		
		payload["segment_index"] += 1

		logger.info(f"Attempting to append segment #{payload['segment_index']} to the media ID:{media_id}.")

		# get current chunk
		if remaining_bytes >= MAX_BYTES_PER_SEG:
			current_chunk = file_content[:MAX_BYTES_PER_SEG]
			file_content = file_content[MAX_BYTES_PER_SEG:]
			remaining_bytes -= MAX_BYTES_PER_SEG
		else:
			current_chunk = file_content
			remaining_bytes = 0

		# send current chunk to twitter
		files = {"media":current_chunk}

		try:
			r = tas.post("https://upload.twitter.com/1.1/media/upload.json", data = payload, files = files)

			if 200 <= r.status_code <= 299:
				logger.info(f"Successfully appended segment #{payload['segment_index']} to the media ID:{media_id}.")

			else:
				logger.critical(f"Failed to append segment #{payload['segment_index']} to the media ID:{media_id}. Reason: {r.status_code} | {r.text}")

		except Exception as e:
			logger.critical(f"Failed to append segment #{payload['segment_index']} to the media ID:{media_id}. Reason: {e}")

		time.sleep(3)

def upload_finalize(tas, media_id):
	logger.info("Upload FINALIZE has started.")

	payload = {
		"command":"FINALIZE", 
		"media_id":media_id
	}

	is_finialized = False

	while not is_finialized:
		r = tas.post("https://upload.twitter.com/1.1/media/upload.json", data = payload)

		if 200 <= r.status_code <= 299:
			resp = json.loads(r.text)
			
			if "processing_info" in resp:
				check_after_time = resp["processing_info"]["check_after_secs"] + 1
				
				logger.info(f"The media associated with media ID:{media_id} is not finalized yet. Checking again in {check_after_time} second(s).")
				
				time.sleep(check_after_time)
			else:
				logger.info(f"The media associated with media ID:{media_id} is finalized and ready for use!")
				is_finialized = True
		
		else:
			logger.critical(f"The media associated with media ID:{media_id} could not be finalized. Reason: {r.status_code} | {r.text}")
			is_finialized = True
	
def get_media_id(tas, file_path):
	media_id = upload_init(tas, file_path)
	upload_append(tas, file_path, media_id)
	upload_finalize(tas, media_id)

	return media_id
