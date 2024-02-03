import logging

from models.timeline_info import TimelineInfo
from service.bing_search import BingSearch
from service.tweet import Tweet
from settings.environ import Environ
import bot_base

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class BotFavorite:
    
    @classmethod
    def check_safe_image_and_favorite(cls, list_id: int, query: str, match_word: str, force=False):
        timeline_info = TimelineInfo.get(list_id, force=force)

        tweet = Tweet()
        timeline = tweet.get_search(query, since_id=timeline_info.since_id).match_filter(match_word=match_word).timeline
        timeline.sort(key=lambda state: state.id)

        for state in timeline:
            if state.media:
                try:
                    matches = sum([BingSearch.visual_search(m.media_url_https) for m in state.media])
                    logger.info(f'{Tweet.parma_link(state)} matches {matches}')
                    if not matches:
                        tweet.create_favorite(state)
                    else:
                        tweet.create_list_member(list_id, state.user.id)
                    timeline_info.put(state.id)
                except Exception as ex:
                    logger.error(ex)


if __name__=="__main__":
    BotFavorite.check_safe_image_and_favorite(Environ.list_id, Environ.query, Environ.match_word, force=Environ.force_update)

