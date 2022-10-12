from flask import Flask
from flask import Response
from flask import request
import spacy
from atis import answer

app = Flask(__name__)
nlp = spacy.load('en_core_web_lg')


@app.route('/', methods=['POST'])
def root():
    response = Response(answer(nlp, request.data.decode()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
