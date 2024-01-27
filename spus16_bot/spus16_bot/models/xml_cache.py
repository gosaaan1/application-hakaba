from sqlalchemy import Column, Integer, String, Text, DateTime, Sequence
from models.sqlalchemy import Base, session
from datetime import datetime

class XmlCache(Base):

    __tablename__ = 'XML_CACHE'

    id = Column(Integer, Sequence('xml_cache_id_seq'), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    xml = Column(Text)
    last_updated = Column('last_updated', DateTime)

    @classmethod
    def get_xml(cls, url:str) -> str:
        r = session.query(cls.xml).filter(cls.url == url).first()
        return r.xml if r else None
    
    @classmethod
    def save_xml(cls, url:str, xml:str) -> None:
        r = session.query(cls).filter(cls.url == url).first()
        if not r:
            r = XmlCache(url=url, last_updated=datetime.now())
        r.xml = xml
        session.add(r)
        session.commit()
