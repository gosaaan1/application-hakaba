import logging
from settings.environ import Environ
import urllib.request
import xml.dom.minidom as md
import xml.dom.minidom as m
import xml.etree.ElementTree as ET

from jma.earthquake_data import JmaXmlData
from models.xml_cache import XmlCache

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class JmaXmlParser:

    def __init__(self, url:str) -> None:
        self.url = url
        self.xml = None
        self.root = None
    
    def _fetch_xml(self) -> str:
        with urllib.request.urlopen(self.url) as response:
            return response.read().decode().replace('\n', '')
    
    def _create_root(self) -> None:
        self.root = ET.fromstring(self.xml)
    
    def parse(self, parser: JmaXmlData) -> dict:
        self.xml = XmlCache.get_xml(self.url)
        if not self.xml:
            self.xml = self._fetch_xml()
            XmlCache.save_xml(self.url, self.xml)
            logger.debug(f'reload from web {self.url}')
        else:
            logger.debug(f'load from cache {self.url}')
        self._create_root()
        return parser.parse(self.root, self.url)
