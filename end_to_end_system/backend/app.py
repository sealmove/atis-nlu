from flask import Flask
from flask import request
import spacy
from atis import answer

app = Flask(__name__)
nlp = spacy.load('en_core_web_lg')

@app.route('/',methods = ['POST'])
def root():
    return answer(nlp, request.data.decode())
