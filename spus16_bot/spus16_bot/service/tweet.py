# import boto3
import logging
import twitter
import re
from settings.environ import Environ
from datetime import datetime, timedelta
import urllib.parse

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class Tweet:

    MESSAGE_MAX_LEN = 144

    @classmethod
    def now(cls, time_delta: timedelta) -> int:
        return (datetime.now() + time_delta).timestamp()

    @classmethod
    def parma_link(cls, s) -> str:
        return f'https://twitter.com/{s.user.screen_name}/status/{s.id}'

    def __init__(self):
        self.__api = twitter.Api(consumer_key=Environ.consumer_key,
                                consumer_secret=Environ.consumer_secret,
                                access_token_key=Environ.access_token_key,
                                access_token_secret=Environ.access_token_secret)
        user = self.__api.VerifyCredentials()
        self.screen_name = user.screen_name if user else None
        self.timeline = []
        self.max_state_id = None

    @classmethod
    def __get_max_state_id(cls, timeline:list) -> int:
        return max([s.id for s in timeline]) if timeline else None
    
    def get_list_timeline(self, list_id: int, since_id=None) -> 'Tweet':
        logger.info(f'list timeline {list_id} since_id {since_id}')
        self.timeline = self.__api.GetListTimeline(list_id, since_id=since_id)
        self.max_state_id = Tweet.__get_max_state_id(self.timeline)
        return self
    
    def get_search(self, query:str, since_id:int=None) -> 'Tweet':
        logger.info(f'search timeline {query} since {since_id}')
        # NOTE since_idが効かない
        self.timeline = [state for state in self.__api.GetSearch(raw_query=f'q={urllib.parse.quote(query)}', since_id=since_id) if not since_id or state.id > since_id]
        self.max_state_id = Tweet.__get_max_state_id(self.timeline)
        return self

    def match_filter(self, match_word:str=None, truncate_timestamp:int=0) -> 'Tweet':
        logger.info(f'match word {match_word}, truncate timestamp {truncate_timestamp}')
        self.timeline = [state for state in self.timeline if (not match_word or re.search(match_word, state.text)) and state.created_at_in_seconds > truncate_timestamp]
        return self
    
    def retweet(self) -> None:
        for status in self.timeline:
            self.__post_retweet(status)

    def __post_retweet(self, status) -> str:
        if not Environ.test_mode:
            self.__api.PostRetweet(status.id)
            logger.info(f'retweet {status.id} {status.text}')
        else:
            logger.info(f'test retweet {status.id} {status.text}')
    
    def create_favorite(self, status):
        if not Environ.test_mode:
            try:
                self.__api.CreateFavorite(status_id=status.id)
                logger.info(f'favorite {Tweet.parma_link(status)}')
            except Exception as ex:
                logger.error(f'favorite error {ex} {Tweet.parma_link(status)}')
        else:
            logger.info(f'test favorite {Tweet.parma_link(status)}')

    def create_list_member(self, list_id: int, user_id: int) -> None:
        self.__api.CreateListsMember(list_id=list_id, user_id=user_id)
        logger.info(f'create list {user_id} to {list_id}')

    def post_tweet(self, message: str, url:str=None):
        if not Environ.test_mode:
            self.__api.PostUpdate(message, attachment_url=url, verify_status_length=True)
        else:
            logger.info(f'PostUpdate {message} {url}')

    def __safe_message(self, message: str) -> str:
        if len(message) <= self.MESSAGE_MAX_LEN:
            return message
        
        pos = message.rfind(' ', 0, self.MESSAGE_MAX_LEN)
        if pos > 0:
            logger.warn(f'truncate message {message}')
            return message[0:pos]
        
        pos = message.rfind('\n', 0, self.MESSAGE_MAX_LEN)
        if pos > 0:
            logger.warn(f'truncate message {message}')
            return message[0:pos]

        raise(f'message too long: {message}')
    
    @classmethod
    def list_to_hashtag(cls, words: list, limit:int=None) -> str:
        if limit:
            logger.debug(f'hashtags {",".join(words)} limit {limit}')
        ws = words[0:limit] if limit and len(words) > limit else words
        return ' '.join([f'#{w}' for w in ws])
