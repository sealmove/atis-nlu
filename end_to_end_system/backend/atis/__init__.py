import json
from sqlite3 import Cursor
from spacy import Language
from atis.intent import *
from atis.entities import *
from atis.actions import *


def parse(nlp: Language, utterance: str) -> str:
    doc = nlp(utterance)
    result = {}
    result['utterance'] = utterance
    result['intent'] = detect_intent(nlp, doc)
    result['entities'] = {}
    locations = extract_locations(nlp, doc)
    airports = extract_airports(nlp, doc)
    if locations:
        result['entities']['locations'] = extract_locations(nlp, doc)
    if airports:
        result['entities']['airports'] = extract_airports(nlp, doc)
    return result


def answer(c: Cursor, nlp: Language, utterance: str) -> str:
    representation = parse(nlp, utterance)
    print(json.dumps(representation, indent=4))
    return action(c, representation)
