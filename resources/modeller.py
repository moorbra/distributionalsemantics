from flask_restful import Resource
from flask import request, jsonify
import requests
import os
import en_core_web_sm
import datetime
import json
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

class Modeller(Resource):
    """Microservice for creating a semantic space from a corpus."""
    corpuspath = ""
    modelname = ""
    nlp = en_core_web_sm.load()
    min_count = 3

    def post(self):
        """Downloads a set of documents from Wikipedia"""
        args = request.get_json(force=True)
        self.corpuspath = args['corpusPath']
        self.modelname = args['modelname']
        documents = self.load_documents()
        sentences = self.tokenize(documents)
        word_vectors = self.create_model(sentences)
        term_list = self.create_term_list(word_vectors)
        self.create_manifest(term_list, len(documents))
        return jsonify({
                'documents' : len(documents),
                'numberterms': len(term_list)
            })

    def create_term_list(self, wordvectors):
        return [term for term, s in wordvectors.vocab.items()]

    def create_manifest(self, terms, numberdocuments):
        manifest = {
            'modelname': self.modelname,
            'terms': terms,
            'numberdocuments': numberdocuments
        }
        with open(os.path.join(self.corpuspath, f"{self.modelname}_manifest.json"), 'w') as mdoc:
            json.dump(manifest, mdoc)
          

    def create_model(self, sentences):
        model = Word2Vec(sentences, size=200, min_count=self.min_count, iter=12)
        model.save(os.path.join(self.corpuspath, self.modelname))
        return model.wv

    def load_documents(self):
        documents = []
        for filename in os.listdir(self.corpuspath):
            if filename.endswith(".txt"):
                with open(os.path.join(self.corpuspath, filename), encoding='utf-8',errors='replace') as fdoc:
                    documents.append(fdoc.read())
        return documents

    def tokenize(self, corpus):        
        sentences = []
        for doc in self.nlp.pipe(corpus, batch_size=10000, n_threads=3):
            for sentence in doc.sents:
                sentences.append([token.lower_ for token in sentence
                                  if not token.is_punct and not token.is_space
                                  and not token.is_stop])
        return sentences


# class SentenceParser(object):
#     def __init__(self, directoryname):
#         self.directoryname = directoryname
#         self.nlp = en_core_web_sm.load()

#     def __iter__(self):
#         for filename in os.listdir(self.directoryname):
#             content = ""
#             with open(os.path.join(self.directoryname, filename)) as fdoc:
#                 content = fdoc.read()

#             for doc in self.nlp.pipe(content, batch_size=10000, n_threads=3):
#                 for sentence in doc.sents:
#                     sentence_tokens = [token.lower_ for token in sentence
#                                        if not token.is_punct and not token.is_space]
#                     yield sentence_tokens

