# XIFY

An API wrapper for Twitter / X made in Python.

## Description

XIFY stands as a powerful Python API wrapper tailored to streamline Twitter integration within your projects. Designed for simplicity without compromising functionality, XIFY facilitates authenticated sessions, ensuring secure and efficient communication with the Twitter API. 

To make note of its foundational capabilities, XIFY empowers users to execute a diverse range of actions, from the creation and deletion of tweets to the seamless uploading of media. Its versatility positions it as a terrific tool for developers seeking to incorporate Twitter functionality into their applications or services.

## Getting Started

### Dependencies

* Python
* certifi
* charset-normalizer
* idna
* oauthlib
* python-dotenv
* requests
* requests-oauthlib
* urllib3

### Installing

* Python can be downloaded from [here](https://www.python.org/)
* Install dependencies using `pip install -r requirements.txt` stored in main project directory.

### Executing program

Below are a few examples of things you can do with this module.

* Creating an instance of XIFY (and authenticating it)
```
from xify import XIFY

def main():
    xify = XIFY()
    xify.create_tas()

if __name__ == "__main__":
    main()
```

* Sending a tweet
```
from xify import XIFY

def main():
    xify = XIFY()
    xify.create_tas()

    message_content = "Hello World!"

    tweet_id = xify.create_tweet(message_content)

if __name__ == "__main__":
    main()
```

* Uploading media to use in a future tweet
```
from xify import XIFY

def main():
    xify = XIFY()
    xify.create_tas()

    file_path = "flower.png"

    media_id = xify.get_media_id(file_path)

    message_content = "A cool picture of a flower!"

    tweet_id = xify.create_tweet(message = message_content, media_ids = media_id)

if __name__ == "__main__":
    main()
```

## Help

* All runtime data of XIFY are stored in the log file located at `storage/logs/xify.logs`.

## Authors

Contributors

* [Filming](https://github.com/filming)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
