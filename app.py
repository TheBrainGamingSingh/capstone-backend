# > $env:FLASK_APP="app"
# > flask run

# > $env:FLASK_DEBUG=1

# python -m venv venv
# venv\Scripts\activate

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
import pickle
import json
import re
import numpy as np

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
words = stopwords.words("english")

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('query')

MODEL_PATH = './model/MultinomialNB.pkl'

with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

with open("./data/mapper.json") as infile:
    label_mapper = json.load(infile)

def clean_and_stem(text):
    return [" ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower() for x in [text]]

# Endpoints
# class ComplaintClassifier(Resource):
#     def get(self):
#         return {'Welcome!': 'This is a sample response of ComplaintClassifier.'}

# api.add_resource(ComplaintClassifier, '/')



# added by Bhardwaj
@app.route("/")
def home():
    return render_template("index.html", flask_token = "Capstone")

class PredictClass(Resource):
    def post(self):
        args = parser.parse_args()
        user_query = clean_and_stem(args['query'])


        label = model.predict(user_query)[0]
        probs = model.predict_proba(user_query)[0]

        prediction = label_mapper[str(label)]
        confidence = int(probs[label] * 10000) / 10000
        output = {'prediction': prediction, 'confidence': confidence}

        return output

api.add_resource(PredictClass, '/predict')

# Users and authentication

db = SQLAlchemy(app)


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
