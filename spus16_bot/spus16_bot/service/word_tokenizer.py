import logging
from abc import ABC

from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from janome.tokenizer import Tokenizer
from settings.environ import Environ

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)
logger.setLevel("DEBUG")

class BaseAnalyzer(ABC):

    TRAFFIC_CHAR_FILTER = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('#|<|>|発生場所:|JR線', '')]
    TRAFFIC_USER_DIC    = './service/user_dic.csv'

    def get_tokens(self, sentence:str) -> list:
        tokens = list(self._analyzer.analyze(sentence))
        for token in tokens:
            logger.debug(f'\ttoken {token}')
        return tokens

class WordFrequencyAnalyzer(BaseAnalyzer):

    def __init__(self, char_filters:list, dictionary:str) -> 'Analyzer':
        tokenizer = Tokenizer(dictionary, udic_type='simpledic', udic_enc='utf8')
        token_filters = [CompoundNounFilter(), TokenCountFilter()]
        self._analyzer = Analyzer(tokenizer=tokenizer, char_filters=char_filters, token_filters=token_filters)

class WordAnalyzer(BaseAnalyzer):

    def __init__(self, char_filters:list, dictionary:str) -> 'Analyzer':
        tokenizer = Tokenizer(dictionary, udic_type='simpledic', udic_enc='utf8')
        # token_filters = [CompoundNounFilter(), POSStopFilter(['記号','助詞'])]
        token_filters = [POSStopFilter(['記号','助詞'])]
        self._analyzer = Analyzer(tokenizer=tokenizer, char_filters=char_filters, token_filters=token_filters)