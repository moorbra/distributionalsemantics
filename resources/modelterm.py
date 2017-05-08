from flask_restful import Resource
from flask import request, jsonify
import requests
import os
import en_core_web_sm
import datetime
import json
import re

class ModelTerm(Resource):
    """Retrieves a sample sentence for a term in a model."""
    MODEL_BASE_DIRECTORY = "wikimodels"

    def get(self, modelname, term):
        return {'exampleSentence': self.find_sentence_for_term(term, modelname)}

    def find_sentence_for_term(self, term, modelname):
        for filename in os.listdir(os.path.join(self.MODEL_BASE_DIRECTORY, modelname)):
            if filename.endswith(".txt"):
                with open(os.path.join(self.MODEL_BASE_DIRECTORY, modelname, filename), 'r', errors='replace') as fdoc:
                    content = fdoc.read()
                    search_result = re.search(f"[^.]*{re.escape(term)}[^.]*\.", content, re.IGNORECASE)
                    if search_result:
                        return search_result[0]
        return f"No sentence found for term '{term}'.'"
