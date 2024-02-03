from jma.jma_xml_data import JmaXmlData

class EarthquakeData(JmaXmlData):

    def parse(self, root, url:str) -> dict:
        head                  = root.find('inf:Head', self.NS)
        headline              = head.find('inf:Headline/inf:Text', self.NS).text
        report_datetime       = head.find('inf:ReportDateTime', self.NS).text
        
        sei_body              = root.find('sei:Body', self.NS)
        comment               = sei_body.find('sei:Comments/sei:ForecastComment/sei:Text', self.NS).text
        observation           = sei_body.find('sei:Intensity/sei:Observation', self.NS)
        prefs                 = {
                                    p.find('sei:Name', self.NS).text: p.find('sei:MaxInt', self.NS).text
                                for p in observation.findall('sei:Pref', self.NS)} if observation else {}

        earth_quake           = sei_body.find('sei:Earthquake', self.NS)
        origin_time           = earth_quake.find('sei:OriginTime', self.NS).text if earth_quake else None
        magnitude             = earth_quake.find('eb1:Magnitude', self.NS).text if earth_quake else None

        area                  = earth_quake.find('sei:Hypocenter/sei:Area', self.NS)
        hypocenter_name       = area.find('sei:Name', self.NS).text if area else None
        hypocenter_coordinate = area.find('jmx_eb:Coordinate', self.NS).text if area else None

        return {
            'place': hypocenter_name,
            'magnitude' : magnitude,
            'coordinate': hypocenter_coordinate,
            'state': f'{headline}{comment}'.strip(),
            'effect': prefs,
            'source': url,
            'origin': origin_time,
            'updated': report_datetime,
        }
