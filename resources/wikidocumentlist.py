"""Wikipedia Document List microservice."""
from flask import request, jsonify
from flask_restful import Resource
import requests
import os
import urllib
import shutil

class WikipediaDocumentList(Resource):
    """Microservice for working with Wikipedia document lists"""

    WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_HEADERS = {'user-agent': 'mooresemantics/1.0.0'}
    WIKI_MODEL_DIRECTORY_ROOT = "wikimodels"
    
    
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

    def post(self):
        """Downloads a set of documents from Wikipedia"""
        args = request.get_json(force=True)
        requested_documents = [document['title'] for document in args['documents']]
        modelname = args['modelName']
        wiki_documents = self.download_documents(requested_documents)
        self.save_wikidocuments(wiki_documents, modelname)
        return jsonify({
            'downloadedDocuments' : len(wiki_documents['pages']) if 'pages' in wiki_documents else 0,
            'corpusPath': os.path.join(self.WIKI_MODEL_DIRECTORY_ROOT, modelname)})

    def save_wikidocuments(self, wiki_documents, modelname):
        """Saves the wiki articles to disk"""
        filepath = os.path.join(self.WIKI_MODEL_DIRECTORY_ROOT,modelname)
        if os.path.exists(filepath):
            shutil.rmtree(filepath)

        os.makedirs(filepath)
        for document in wiki_documents['pages']:
            if 'extract' in document:
                filename =(f"{document['pageid']}.txt")         
                with open(os.path.join(filepath,filename), 'w', encoding='utf-8') as fdoc:
                    fdoc.write(str.encode(document['extract'], errors='replace').decode("utf-8"))


    def download_documents(self, documents):
        """Downloads documents from Wikipedia"""
        parameters = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext':True,
            'titles': str.join('|', documents),
            'exsectionformat': 'plain',
            'exintro': True
        }

        result = requests.get(self.WIKI_API_BASE_URL,
                              params=parameters,
                              headers=self.WIKI_HEADERS).json()

        if 'error' in result:
            raise Exception(result['error'])

        return result['query']        
