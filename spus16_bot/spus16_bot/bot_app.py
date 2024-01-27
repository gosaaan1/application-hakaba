from datetime import timedelta
import logging

from crawler.train_state_crawler import TrainStateCrawler
from crawler.jma_crawler import JmaCrawler
from jma.jma_xml_parser import JmaXmlParser
from jma.earthquake_data import EarthquakeData
from settings.environ import Environ
from models.sqlalchemy import ENGINE, Base
from service.tweet import Tweet
from models.train_state import TrainState
from models.timeline_info import TimelineInfo
from service.tineye import Tineye

# SEE https://docs.python.org/ja/3/library/logging.html
logging.basicConfig(format='%(asctime)-15s %(levelname)s %(module)s:%(lineno)d %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class BotApp:

    @classmethod
    def run(cls):
        # BotApp.retweet_from_list(1409874535810273281, '遅れ|見合わせ')
        # BotApp.retweet_from_list(1410025906286981122, 'M[5|6|7]')
        BotApp.tineye_check(1410600878831112193, 'このお題で呟怖をください')

        messages = [
            # *BotApp.train_state_crawler(),
            # *BotApp.jma_earthquake_alert(),
        ]

        for message in messages:
            Tweet().post_tweet(message)

    @classmethod
    def train_state_crawler(cls):
        messages = []
        crawler = TrainStateCrawler()
        new_state = crawler.reload().arrival(force=True, datetime_key='published_parsed').sort_by_datetime(datetime_key='published_parsed').to_state()
        if crawler.state:
            # NOTE Atomのupdatedがあてにならないので前回と差分をとって最新のフィードを判定
            arrivals = new_state.keys() - crawler.state.keys()
            for key in arrivals:
                e = new_state[key]
                company = Tweet.list_to_hashtag(e["company"], limit=1)
                effect = Tweet.list_to_hashtag(e["effect"])
                message = f'🚃#列車運行情報 {company} {effect} の情報が新たに掲載されています({e["state"]})\n{e["source"]}'
                messages.append(message)
        else:
            logger.debug(f'publish skipped {new_state}')

        for s in new_state.values():
            html = TrainState.fetch_html(s["source"])
            TrainState.save_html(s["source"], html)

        crawler.save(new_state)
        return messages
    
    @classmethod
    def jma_earthquake_alert(cls):
        messages = []
        all_docs = []
        crawler = JmaCrawler()
        # TODO 動作確認のために force=True にしています
        new_entries = crawler.reload().arrival(force=True).select_by(titles=['震源に関する情報', '震源・震度に関する情報']).sort_by_datetime().entries
        if new_entries:
            # TODO JmaXmlParserにXMLドキュメントをキャッシュする仕組みをつける
            all_docs = [JmaXmlParser(e.link).parse(EarthquakeData()) for e in new_entries]
            essential_docs = {d['place']:d for d in all_docs if int(d['magnitude'][0:1]) >=5}.values()
            for d in essential_docs:
                effects = Tweet.list_to_hashtag(list(d['effect'].keys()))
                message = f'#地震速報 #{d["place"]} {d["state"]} {effects}'
                messages.append(message)
        crawler.save(all_docs)
        return messages
    
    @classmethod
    def retweet_from_list(cls, list_id: int, match_word:str, force: bool=False) -> None:
        timeline_info = TimelineInfo.get(list_id, force=force)

        tweet = Tweet()
        tweet.get_list_timeline(list_id, since_id=timeline_info.since_id)\
            .match_filter(match_word=match_word, truncate_timestamp=Tweet.now(timedelta(minutes=-15)))\
            .retweet()

        timeline_info.put(tweet.max_state_id)

    @classmethod
    def __reject_duplicate_text(cls, state_list:list) -> list:
        d = {}
        for s in state_list:
            # TODO 微妙な言い回しの違いは除外できない
            if d.get(s.text):
                break
            d[s.text] = s
        r = list(d.values())
        logger.debug(f'reject {len(state_list) - len(r)}')
        return r

    @classmethod
    def tineye_check(cls, list_id: int, match_word):
        tweet = Tweet()
        timeline = tweet.get_list_timeline(list_id).match_filter(match_word=match_word).timeline
        for state in timeline:
            matches = sum([Tineye.get_num_matches(m.media_url_https) for m in state.media])
            print(f'{state.id} matches {matches}')
            if not matches:
                tweet.create_favorite(state.id)



Base.metadata.create_all(ENGINE)

if __name__=="__main__":
    BotApp.run()
