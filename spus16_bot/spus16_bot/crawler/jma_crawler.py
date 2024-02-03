from crawler.base_crawler import BaseCrawler

class JmaCrawler(BaseCrawler):

    EQ_RSS_URL = 'http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml'
    LEQ_RSS_URL = 'http://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml'

    URL = EQ_RSS_URL
    STATE_KEY = 'jma_earthquake'

    def to_state(self) -> dict:
        state = {}
        for entry in self.entries:
            state[entry.link] = {
                'title': entry.title,
                'state':   entry.summary,
                'source':  entry.link,
                'updated': entry.updated
            }
        
        return state
