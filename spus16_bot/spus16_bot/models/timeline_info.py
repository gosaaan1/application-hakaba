from sqlalchemy import Column, Integer, String, Text, DateTime, Sequence
from models.sqlalchemy import Base, session
from datetime import datetime
import urllib.request
import logging
from settings.environ import Environ

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class TimelineInfo(Base):

    __tablename__ = "TIMELINE_INFO"

    id = Column(Integer, primary_key=True)
    since_id = Column(Integer)
    last_updated = Column('last_updated', DateTime)

    @classmethod
    def get(cls, id: int, force=False) -> 'TimelineInfo':
        timeline_info = session.query(cls).filter(cls.id == id).first()
        if timeline_info and force:
            timeline_info.since_id = None
        return timeline_info if timeline_info else TimelineInfo(id=id)
    
    def put(self, max_state_id: int) -> None:
        if max_state_id:
            self.since_id = max_state_id
        self.last_updated = datetime.now()
        session.add(self)
        session.commit()

