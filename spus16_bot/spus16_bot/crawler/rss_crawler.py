import logging
from datetime import datetime, timedelta
from typing import List

import feedparser
from models.state import State
from settings.environ import Environ

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class RssCrawler:

    def __init__(self, state_key: str, rss_url: str) -> None:
        self._state_key = state_key
        self._rss_url = rss_url
        self._current_state = State.load(self._state_key)
        self._doc = None
        self._last_updated = None
        self.entries = []

    @property    
    def state(self) -> dict:
        return self._current_state.state()

    def save(self, state:dict) -> None:
        self._current_state.save(state, self._last_updated)
    
    def reload(self, datetime_key:str='updated_parsed') -> 'RssCrawler':
        self._doc = feedparser.parse(self._rss_url)
        self.entries = self._doc.entries
        self._last_updated = datetime(*self._doc.feed.get(datetime_key)[:6])
        # logger.info(f'fetch {self._rss_url} last_updated {self._last_updated}')
        return self

    def arrival(self, force=False, datetime_key:str='updated_parsed') -> 'RssCrawler':
        if force or self._current_state.last_updated is None:
            self.entries = [e for e in self._doc.entries]
        else:
            self.entries = [e for e in self._doc.entries if datetime(*e.get(datetime_key)[:6]) > self._current_state.last_updated]
        return self

    def select_by(self, titles: List[str]) -> 'RssCrawler':
        self.entries = [e for e in self.entries if e.title in titles]
        return self
    
    def sort_by_datetime(self, datetime_key:str='updated_parsed') -> 'RssCrawler':
        self.entries.sort(key=lambda e: datetime(*e.get(datetime_key)[:6]))
        return self
