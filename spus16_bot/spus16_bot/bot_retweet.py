import logging
from datetime import timedelta

from models.timeline_info import TimelineInfo
from service.tweet import Tweet
from settings.environ import Environ
from crawler.train_state_crawler import TrainStateCrawler
import bot_base

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class BotRetweet:
    
    @classmethod
    def retweet_from_list(cls, list_id: int, match_word:str, force: bool=False) -> None:
        timeline_info = TimelineInfo.get(list_id, force=force)

        tweet = Tweet()
        timeline = tweet.get_list_timeline(list_id, since_id=timeline_info.since_id)\
                        .match_filter(match_word=match_word, truncate_timestamp=Tweet.now(timedelta(minutes=-30)))
        
        for state in timeline:
            if timeline_info.since_id:
                state.retweet()

        timeline_info.put(tweet.max_state_id)

if __name__=="__main__":
    BotRetweet.retweet_from_list(Environ.list_id, Environ.match_word, force=Environ.force_update)
