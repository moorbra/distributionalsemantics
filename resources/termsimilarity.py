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

    def get(self, modelname, term):
        self.modelname = modelname
        model = self.load_model(modelname)
        similar_terms = self.get_similar_terms(model, term)
        return {
            'term': term,
            'sentence': self.find_sentence_for_term(term),
            'similarterms' : similar_terms
        }

    def get_similar_terms(self, model, term):
        # similar_terms = []
        # for word, similarity in model.most_similar(positive=[term], topn=10):
        #     similar_terms.append({ 'term' : word, 'similarity': similarity, 'sentence': self.find_sentence_for_term(word) })
        # return similar_terms
        return [{ 'term' : word, 'similarity': similarity, 'sentence': self.find_sentence_for_term(word) } for word, similarity in model.most_similar(positive=[term], topn=10)]

    def load_model(self, modelname):
        return Word2Vec.load(os.path.join(self.MODEL_BASE_DIRECTORY, modelname, modelname)).wv

    def find_sentence_for_term(self, term):
        for filename in os.listdir(os.path.join(self.MODEL_BASE_DIRECTORY, self.modelname)):
            if filename.endswith(".txt"):
                with open(os.path.join(self.MODEL_BASE_DIRECTORY, self.modelname, filename), 'r', errors='replace') as fdoc:
                    content = fdoc.read()
                    search_result = re.search(f"[^.]*{re.escape(term)}[^.]*\.", content, re.IGNORECASE)
                    if search_result:
                        return search_result[0]
        return f"No sentence found for term '{term}'.'"
