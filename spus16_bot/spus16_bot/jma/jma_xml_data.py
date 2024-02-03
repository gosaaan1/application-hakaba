from abc import ABC, abstractmethod

class JmaXmlData(ABC):

    NS = {
        'inf': 'http://xml.kishou.go.jp/jmaxml1/informationBasis1/',
        'met': 'http://xml.kishou.go.jp/jmaxml1/body/meteorology1/',
        'sei': 'http://xml.kishou.go.jp/jmaxml1/body/seismology1/',
        'eb1': 'http://xml.kishou.go.jp/jmaxml1/elementBasis1/',
        'jmx_eb': "http://xml.kishou.go.jp/jmaxml1/elementBasis1/"
    }

    @abstractmethod
    def parse(self):
        pass

