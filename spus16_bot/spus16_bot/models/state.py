import json
from sqlalchemy import Column, Integer, String, Text, DateTime, Sequence
from models.sqlalchemy import Base, session
from datetime import datetime

class State(Base):

    __tablename__ = 'STATE'

    id = Column(Integer, Sequence('state_id_seq'), primary_key=True)
    state_key = Column(String, nullable=False, unique=True)
    state_json = Column(Text)
    last_updated = Column('last_updated', DateTime)

    @classmethod
    def load(cls, state_key: str) -> 'State':
        state = session.query(cls).filter(cls.state_key == state_key).first()
        return state if state else State(state_key=state_key)
    
    def state(self) -> dict:
        return json.loads(self.state_json) if self.state_json else {}
    
    def save(self, current_state: dict, last_updated: datetime) -> None:
        self.state_json = json.dumps(current_state)
        self.last_updated = last_updated
        session.add(self)
        session.commit()
