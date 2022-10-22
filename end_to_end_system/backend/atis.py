from typing import Optional
from enum import Enum, auto
import json
import spacy
from spacy.tokens import Doc
from spacy.matcher import Matcher


class Intent(Enum):
    CHEAPEST = auto()
    MOST_EXPENSIVE = auto()
    AIRPORT_CODE = auto()
    CITY = auto()
    FLIGHT = auto()


def extract_locations(nlp: spacy.Language, doc: Doc) -> dict:
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'ADP'}, {'ENT_TYPE': 'GPE'}]
    matcher.add('Location', [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    locations = {l[0].text: l[1].text for l in spans}
    return locations


def extract_airports(nlp: spacy.Language, doc: Doc) -> dict:
    matcher = Matcher(nlp.vocab)
    pattern = [{'TEXT': {'REGEX': '[A-Z]{3}'}}]
    matcher.add('Airports', [pattern])
    matches = matcher(doc)
    airports = [doc[start:end].text for _, start, end in matches]
    return airports


def detect_intent(doc: Doc) -> Optional[Intent]:
    dobjs_filter = filter(lambda token: token.dep_ == 'dobj', list(doc))
    dobjs = list(dobjs_filter)
    if dobjs:
        # verb = dobjs[0].head
        dobj = dobjs[0]
    else:
        return None

    # Extract the intent verb
    # helperVerbList = ['want', 'like', 'need', 'order']
    # if verb.text in helperVerbList:
    #     intentVerb = verb
    # elif verb.head.dep_ == 'ROOT':
    #     intentVerb = verb.head

    intentObj = dobj

    # Extract the object of the intent
    # intentObj = None
    objList = ['flight', 'ticket']
    if dobj.text in objList:
        intentObj = dobj
    else:
        for child in dobj.children:
            if child.dep_ == 'prep':
                intentObj = list(child.children)[0]
                break
            elif child.dep_ == 'compound':
                intentObj = child
                break

    objSynset = ('flight', 'ticket')

    return Intent.FLIGHT if intentObj.lemma_ in objSynset else None


def answer(nlp: spacy.Language, utterance: str) -> str:
    # normalize
    doc = nlp(utterance)
    locations = extract_locations(nlp, doc)
    airports = extract_airports(nlp, doc)
    return 'Google it' if not airports else json.dumps(airports)


nlp = spacy.load('en_core_web_lg')
# utterance = 'find a flight from washington to sf'
utterance = 'i want to make a reservation for a flight'
doc = nlp(utterance)
x = detect_intent(doc)
print(x)
