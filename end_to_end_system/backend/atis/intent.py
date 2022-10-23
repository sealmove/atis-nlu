from typing import Optional
from enum import Enum
from spacy.tokens import Doc


class Intent(str, Enum):
    CHEAPEST = 'find_cheapest_flight'
    MOST_EXPENSIVE = 'find_most_expensive_flight'
    AIRPORT_CODE = 'find_airport_code'
    CITY = 'find_city_of_airport'
    FLIGHT = 'find_flight'


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
