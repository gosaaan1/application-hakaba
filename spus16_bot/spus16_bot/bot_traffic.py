import logging
import re

from models.timeline_info import TimelineInfo
from service.tweet import Tweet
from settings.environ import Environ
from service.word_tokenizer import WordFrequencyAnalyzer
import bot_base

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class BotTraffic:
    
    @classmethod
    def retweet_from_list(cls, list_id: int, place_words:str=None, state_words:str=None, force: bool=False) -> None:
        timeline_info = TimelineInfo.get(list_id, force=force)

        analyzer = WordFrequencyAnalyzer(WordFrequencyAnalyzer.TRAFFIC_CHAR_FILTER, WordFrequencyAnalyzer.TRAFFIC_USER_DIC)

        tweet = Tweet()
        timeline = tweet.get_list_timeline(list_id, since_id=timeline_info.since_id).timeline
        logger.info(f'timeline {len(timeline)}')

        summary = {}
        for s in sorted(timeline, key=lambda x: x.id):
            logger.info(f'{s.id}, {s.user.screen_name}, {s.hashtags}, {s.urls}')
            logger.info(f'{s.text}')

            tokens = analyzer.get_tokens(s.text)

            places = [t for t in tokens if re.search(place_words, t[0])]
            states = [t for t in tokens if re.search(state_words, t[0])]
            logger.debug(f'\tplaces {places}')
            logger.debug(f'\tstates {states}')

            if places and states:
                line = places[0][0]
                item = summary.get(line, {
                    'screen_names': set(),
                    'states': None,
                    'state_id': None,
                    'parma_link': None,
                })
                item['screen_names'].add(s.user.screen_name)
                item['states'] = states
                item['state_id'] = s.id
                item['parma_link'] = Tweet.parma_link(s)
                summary[line] = item
        
        logger.info(f'summary {len(summary.keys())} {summary}')

        for line, item in summary.items():
            # screen_names = [f'@{screen_name}' for screen_name in item['screen_names']]
            # append_message = f' 詳細は公式アカウントからご確認ください。 {" ".join(screen_names)}' if len(screen_names) > 1 else ''
            # message = f'#運行情報 #{line} に遅延、運休などが発生しています。{append_message}'
            message = f'#運行情報 #{line} に遅延、運休などが発生しています。'
            if timeline_info.since_id:
                tweet.post_tweet(message, url=item['parma_link'])

        timeline_info.put(tweet.max_state_id)

if __name__=="__main__":
    BotTraffic.retweet_from_list(Environ.list_id, place_words=Environ.place_words, state_words=Environ.state_words, force=Environ.force_update)
