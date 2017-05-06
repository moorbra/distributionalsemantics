"""Wikipedia microservice."""
from flask_restful import Resource
import requests

class WikipediaCategory(Resource):
    """Microservice for working with Wikipedia article catagories"""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_HEADERS = {'user-agent': 'mooresemantics/1.0.0'}  

    def get(self, startswith='a'):
        """Blah"""
        resource_url = f"{self.WIKI_API_BASE_URL}?action=query&format=json&list=allcategories&aclimit=200&acmin=10&acprefix={startswith}"
        resp = requests.get(resource_url, headers=self.WIKI_HEADERS)

        if resp.status_code != 200:
            raise Exception("Error response from data source")

        json = resp.json()        
        return json['query']['allcategories']
    