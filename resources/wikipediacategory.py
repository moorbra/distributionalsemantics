"""Wikipedia microservice. """
from flask_restful import Resource
import requests

class WikipediaCategory(Resource):
    """Microservice for working with Wikipedia article catagories"""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_USER_AGENT = {'user-agent': 'mooresemantics/1.0.0' }

    def get(self):
        #r = requests.get(url, headers=headers)
        return { 'Hello': 'World' }

    def post(self):
        pass
    