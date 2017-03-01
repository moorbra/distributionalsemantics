"""Wikipedia microservice. """
from flask_restful import Resource

class WikipediaCategory(Resource):
    """Microservice for working with Wikipedia article catagories"""
    def get(self):
        return { 'Hello': 'World' }

    def post(self):
        pass
    