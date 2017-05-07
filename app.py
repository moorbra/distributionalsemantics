"""Semantics Api"""
from flask import Flask, url_for, render_template
from flask_restful import Api
from resources.wikipediacategory import WikipediaCategory
from resources.wikidocumentlist import WikipediaDocumentList
from resources.wikidocument import WikipediaDocument

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wikipedia')
def wikipedia():
    return render_template('wikipedia.html')

api.add_resource(WikipediaCategory, '/wikipedia/categories',
                 '/wikipedia/categories/<string:startswith>')

api.add_resource(WikipediaDocumentList, '/wikipedia/documentlist/<string:category>')
api.add_resource(WikipediaDocument, '/wikipedia/document/<string:document_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
