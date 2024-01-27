import re

from crawler.base_crawler import BaseCrawler


class TrainStateCrawler(BaseCrawler):

    URL = 'http://api.tetsudo.com/traffic/rss20.xml'
    STATE_KEY = 'train_state_crawler'

    def to_state(self) -> dict:
        state = {}
        for entry in self.entries:
            parsed_title = re.split('【|】', entry.title)
            company = parsed_title[1]
            lines = parsed_title[2].split('・')
            state_time = re.search(r'\d{1,2}:\d{2}現在', entry.summary)
            state[company] = {
                'company': [company],
                'state':   state_time.group() if state_time else None,
                'source':  entry.link,
                'effect':  lines,
                'updated': entry.updated
            }
        
        return state
