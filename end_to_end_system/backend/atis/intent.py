from typing import Optional
from enum import Enum
from spacy import Language
from spacy.tokens import Doc
from spacy.matcher import DependencyMatcher


class Intent(str, Enum):
    CHEAPEST = 'find_cheapest_flight'
    MOST_EXPENSIVE = 'find_most_expensive_flight'
    AIRPORT_CODE = 'find_airport_code'
    CITY = 'find_city_of_airport'
    FLIGHT = 'find_flight'


def get_adjectives(nlp: Language, doc: Doc):
    pattern = [
        {
            "RIGHT_ID": "target",
            "RIGHT_ATTRS": {"POS": "NOUN"}
        },
        {
            "LEFT_ID": "target",
            "REL_OP": ">",
            "RIGHT_ID": "modifier",
            "RIGHT_ATTRS": {"DEP": {"IN": ["amod"]}}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    return [(doc[target], doc[modifier]) for _, (target, modifier) in matcher(doc)]


def detect_intent(nlp: Language, doc: Doc) -> Optional[Intent]:
    dobjs_filter = filter(lambda token: token.dep_ == 'dobj', list(doc))
    dobjs = list(dobjs_filter)
    dobj = dobjs[0]

    intentObj = dobj

    # Extract the object of the intent
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

    adjectives = get_adjectives(nlp, doc)
    for (target, modifier) in adjectives:
        if intentObj == target:
            if modifier.lemma_ == 'cheap':
                return Intent.CHEAPEST
