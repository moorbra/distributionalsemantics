from flask_restful import Resource
from flask import request, jsonify
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
import requests
import os
import en_core_web_sm
import datetime
import json
import re

class TermSimilarity(Resource):
    MODEL_BASE_DIRECTORY = "wikimodels"
    modelname = ""

    def get(self, modelname, term, direction="positive"):
        self.modelname = modelname
        model = self.load_model()
        similar_terms = self.get_similar_terms(model, [term], direction)
        return {
            'direction': direction,
            'term': term,
            'sentence': self.find_sentence_for_term(term),
            'similarterms' : similar_terms
        }

    def post(self):
        args = request.get_json(force=True)
        self.modelname = args['modelname']
        model = self.load_model()        
        similar_terms = self.get_similar_terms(model, args['terms'], args['direction'])
        return {
            'direction': args['direction'],
            'terma': args['terms'][0],
            'termb': args['terms'][1],
            'sentenceTerma': self.find_sentence_for_term(args['terms'][0]),
            'sentenceTermb': self.find_sentence_for_term(args['terms'][1]),
            'similarterms' : similar_terms
        }        

    def get_similar_terms(self, model, terms, direction):
        if direction == "positive":
            return [{ 'term' : word, 'similarity': similarity, 'sentence': self.find_sentence_for_term(word) } for word, similarity in model.most_similar(positive=terms, topn=10)]

        return [{ 'term' : word, 'similarity': similarity, 'sentence': self.find_sentence_for_term(word) } for word, similarity in model.most_similar(negative=terms, topn=10)]
        

    def load_model(self):
        return Word2Vec.load(os.path.join(self.MODEL_BASE_DIRECTORY, self.modelname, self.modelname)).wv

    def find_sentence_for_term(self, term):
        for filename in os.listdir(os.path.join(self.MODEL_BASE_DIRECTORY, self.modelname)):
            if filename.endswith(".txt"):
                with open(os.path.join(self.MODEL_BASE_DIRECTORY, self.modelname, filename), 'r', errors='replace') as fdoc:
                    content = fdoc.read()
                    search_result = re.search(f"[^.]*{re.escape(term)}[^.]*\.", content, re.IGNORECASE)
                    if search_result:
                        return search_result[0]
        return f"No sentence found for term '{term}'.'"
