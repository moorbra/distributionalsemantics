from flask_restful import Resource
from flask import request, jsonify
import requests
import os
import en_core_web_sm
import datetime
import json
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

class ModelManifest(Resource):
    MODEL_BASE_DIRECTORY = "wikimodels"

    def get(self, modelname=None):
        if modelname is None:
            return self.get_model_manifests()
        return self.get_model_manifest(modelname)

    def get_model_manifest(self, modelname):
        for filename in os.listdir(os.path.join(self.MODEL_BASE_DIRECTORY, modelname)):
            if filename.endswith(".json"):
                with open(os.path.join(self.MODEL_BASE_DIRECTORY, modelname, filename), 'r') as fManifest:
                    return json.loads(fManifest.read())

    def get_model_manifests(self):
        manifests = []
        model_directories = [directory for directory in os.listdir(self.MODEL_BASE_DIRECTORY)]
        for directory in model_directories:
            for filename in os.listdir(os.path.join(self.MODEL_BASE_DIRECTORY, directory)):
                if filename.endswith(".json"):
                    with open(os.path.join(self.MODEL_BASE_DIRECTORY, directory, filename), 'r') as fManifest:
                        manifest = json.loads(fManifest.read())
                        manifests.append({
                            'modelname': manifest['modelname'],
                            'terms': len(manifest['terms']),
                            'numberdocuments': manifest['numberdocuments']
                        })
        return manifests
