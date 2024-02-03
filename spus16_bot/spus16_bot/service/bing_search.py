import json
import logging

import requests
from settings.environ import Environ

logger = logging.getLogger(__name__)
logger.setLevel(Environ.log_level)

class BingSearch:

    BASE_URI = 'https://api.bing.microsoft.com/v7.0/images/visualsearch'
    HEADERS = {'Ocp-Apim-Subscription-Key': Environ.subscription_key}

    @classmethod
    def visual_search(cls, image_url:str) -> int:
        logger.debug(f'\tvisual search {image_url}')

        data = {
            'imageInfo': {
                'url': image_url
            }
        }
        payload = {'knowledgeRequest': json.dumps(data)}
        response = requests.post(cls.BASE_URI, headers=cls.HEADERS, files=payload)
        response.raise_for_status()
        result = response.json()
        logger.debug(f'result: {result}')
        for tag in result['tags']:
            for action in tag['actions']:
                if action['actionType'] == 'PagesIncluding':
                    return len(action['data']['value'])
        return 0
