from abc import abstractmethod
from crawler.rss_crawler import RssCrawler

class BaseCrawler(RssCrawler):

    URL = None
    STATE_KEY = None

    def __init__(self):
        super(BaseCrawler, self).__init__(self.STATE_KEY, self.URL)

    @classmethod
    @abstractmethod
    def entries_to_state(self, entries:list) -> dict:
        pass