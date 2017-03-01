"""Semantics Api"""
from flask import Flask
from flask_restful import Api
from resources.wikipediacategory import WikipediaCategory

app = Flask(__name__)
api = Api(app)

api.add_resource(WikipediaCategory, '/semantics/categories', endpoint='categories')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
