from sqlalchemy import Column, Integer, String, Text, DateTime, Sequence
from models.sqlalchemy import Base, session
from datetime import datetime
import urllib.request
import logging
from settings.environ import Environ

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class TrainState(Base):

    __tablename__ = "TRAIN_STATE"

    id = Column(Integer, Sequence('train_state_id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    html = Column(Text)
    last_updated = Column('last_updated', DateTime)

    @classmethod
    def fetch_html(cls, url:str) -> str:
        try:
            logger.info(f'fetch from {url}')
            with urllib.request.urlopen(url, timeout=30) as response:
                charset = response.info().get_content_charset()
                if charset:
                    return response.read().decode(charset)
                else:
                    return response.read().decode()
        except Exception as e:
            logger.error(f'{e} in {url}')

    @classmethod
    def save_html(cls, url:str, html:str) -> None:
        r = session.query(cls).filter(cls.url == url).first()
        if not r:
            r = TrainState(url=url)
        r.html = html
        r.last_updated = datetime.now()
        session.add(r)
        session.commit()
