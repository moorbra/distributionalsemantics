"""Wikipedia Categories microservice."""
from flask_restful import Resource
import requests

class WikipediaCategory(Resource):
    """Microservice for working with Wikipedia article catagories"""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_HEADERS = {'user-agent': 'mooresemantics/1.0.0'}

    def get(self, startswith='a'):
        """Returns a list of Wikipedia categories"""
        parameters = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'acprefix': startswith,
            'list': 'allcategories',
            'aclimit': 'max',
            'acprop': 'size'
        }
        result = requests.get(self.WIKI_API_BASE_URL,
                              params=parameters,
                              headers=self.WIKI_HEADERS).json()

        if 'error' in result:
            raise Exception(result['error'])

        return [category for category in result['query']['allcategories']
                if category['size'] > 0 and category['pages'] > 0]
    