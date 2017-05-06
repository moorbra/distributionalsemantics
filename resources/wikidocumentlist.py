"""Wikipedia Document List microservice."""
from flask_restful import Resource
import requests
import urllib

class WikipediaDocumentList(Resource):
    """Microservice for working with Wikipedia document lists"""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_HEADERS = {'user-agent': 'mooresemantics/1.0.0'}
    
    def get(self, category):
        """Returns all the documents for a given category"""
        parameters = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'cmtitle': f"Category:{category}",
            'list': 'categorymembers',
            'cmlimit': 'max'
        }
        result = requests.get(self.WIKI_API_BASE_URL,
                              params=parameters,
                              headers=self.WIKI_HEADERS).json()

        if 'error' in result:
            raise Exception(result['error'])

        return result['query']  
