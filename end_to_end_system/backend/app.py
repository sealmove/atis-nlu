from flask import Flask
from flask import Response
from flask import request
import spacy
import sqlite3
from atis import answer

app = Flask(__name__)
nlp = spacy.load('en_core_web_lg')
conn = sqlite3.connect('flights.db', check_same_thread=False)
c = conn.cursor()


@app.route('/', methods=['POST'])
def root():
    response = Response(answer(c, nlp, request.data.decode()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
