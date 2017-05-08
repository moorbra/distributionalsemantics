"""Semantics Api"""
from flask import Flask, url_for, render_template
from flask_restful import Api
from resources.wikipediacategory import WikipediaCategory
from resources.wikidocumentlist import WikipediaDocumentList
from resources.wikidocument import WikipediaDocument
from resources.modeller import Modeller
from resources.modelmanifest import ModelManifest
from resources.modelterm import ModelTerm
from resources.termsimilarity import TermSimilarity

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wikipedia')
def wikipedia():
    return render_template('wikipedia.html')

@app.route('/models')
def models():
    return render_template('models.html')

api.add_resource(WikipediaCategory, '/wikipedia/categories',
                 '/wikipedia/categories/<string:startswith>')

api.add_resource(WikipediaDocumentList, '/wikipedia/documentlist/<string:category>',
                 '/wikipedia/documentlist')

api.add_resource(WikipediaDocument, '/wikipedia/document/<string:document_id>')

api.add_resource(Modeller, '/modeller/createmodel')

api.add_resource(ModelManifest, '/manifest/manifests',
                 '/manifest/manifests/<string:modelname>')

api.add_resource(ModelTerm, '/term/<string:modelname>/<string:term>')

api.add_resource(TermSimilarity, '/similarity/<string:modelname>/<string:term>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
