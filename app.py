"""Semantics Api"""
from flask import Flask, url_for, render_template
from flask_restful import Api
from resources.wikipediacategory import WikipediaCategory

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(WikipediaCategory, '/semantics/categories',
                 '/semantics/categories/<string:startswith>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
