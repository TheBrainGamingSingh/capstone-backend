# > $env:FLASK_APP="app"
# > flask run

# > $env:FLASK_DEBUG=1

# python -m venv venv
# venv\Scripts\activate

from flask import Flask, render_template, url_for, make_response
# from flask_sqlalchemy import SQLAlchemy
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

MODEL_PATH = './model/RBF_SVC.pkl'

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



#added by Bhardwaj
@app.route("/")
def home():
    return render_template("index.html", flask_token = "Capstone")

# TODO: Put this in a try except block to report errors
class PredictClass(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        text_query = str(args['query'])
        print(text_query)
        user_query = clean_and_stem(text_query)


        label = model.predict(user_query)[0]
        probs = model.predict_proba(user_query)[0]

        labels = [(i, label_mapper[str(i)], probs[i]) for i in sorted(range(len(probs)), key = lambda i: probs[i],reverse=True)][:3]
        labels_dict = []

        for i in labels:
            j = {}
            j['id'] = i[0]
            j['category'] = i[1]
            j['confidence'] = i[2]

            labels_dict.append(j)

        prediction = label_mapper[str(label)]
        confidence = int(probs[label] * 10000) / 10000

        # return the prediction, confidence and top three labels
        output = {'text_query' : text_query, 'prediction': prediction, 'confidence': confidence, 'labels' : labels_dict}
        return output


# api.add_resource(PredictClass, '/api/predict')
api.add_resource(PredictClass, '/predict')


# Users and authentication

# db = SQLAlchemy(app)


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
