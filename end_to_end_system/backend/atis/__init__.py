import json
from spacy import Language
from atis.intent import *
from atis.entities import *


def answer(nlp: Language, utterance: str) -> str:
    # normalize
    doc = nlp(utterance)
    result = {}
    result['utterance'] = utterance
    result['intent'] = detect_intent(doc)
    result['entities'] = {}
    locations = extract_locations(nlp, doc)
    airports = extract_airports(nlp, doc)
    if locations:
        result['entities']['locations'] = extract_locations(nlp, doc)
    if airports:
        result['entities']['airports'] = extract_airports(nlp, doc)
    return result
    # return 'Google it' if not airports else json.dumps(airports)
