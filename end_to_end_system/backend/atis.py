import spacy
from spacy.matcher import Matcher
import json

def extract_location_entities(nlp, doc):
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'ADP'}, {'ENT_TYPE': 'GPE'}]
    matcher.add('Location', [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for mid, start, end in matches]
    locations = {l[0].text: l[1].text for l in spans}
    return locations

def answer(nlp, utterance):
    doc = nlp(utterance)
    return json.dumps(extract_location_entities(nlp, doc))
