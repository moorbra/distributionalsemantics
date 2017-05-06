"""Wikipedia Document microservice."""
from flask_restful import Resource
import requests

class WikipediaDocument(Resource):
    """Microservice for working with a Wikipedia document."""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_HEADERS = {'user-agent': 'mooresemantics/1.0.0'}

    def get(self, document_id):
        """Returns a wikipedia document"""
        parameters = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext':True,
            'titles': document_id,
            'exsectionformat': 'plain'
        }

        result = requests.get(self.WIKI_API_BASE_URL,
                              params=parameters,
                              headers=self.WIKI_HEADERS).json()

        if 'error' in result:
            raise Exception(result['error'])

        return result['query']
