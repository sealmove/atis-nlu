from typing import Optional
from spacy import Language
from spacy.tokens import Doc
from spacy.tokens import Token
from spacy.matcher import DependencyMatcher
from atis.types import *


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


def get_dobj(doc: Doc) -> Token:
    dobjs_filter = filter(lambda token: token.dep_ == 'dobj', list(doc))
    dobjs = list(dobjs_filter)
    return dobjs[0] if dobjs else None


# Need fix: To be generic (not only specific to Intent.FLIGHT)
def get_delegated_intent_obj(dobj: Token) -> Token:
    objList = ['flight', 'ticket', 'fare', 'airfare', 'city', 'airport']
    if dobj.text in objList:
        return dobj
    else:
        for child in dobj.children:
            if child.dep_ == 'prep':
                return list(child.children)[0]
            elif child.dep_ == 'compound':
                return child


def obj_has_adjective(obj: Token, adjectives: list[tuple[Token, Token]], adjective: str) -> bool:
    for (target, modifier) in adjectives:
        if obj == target:
            if modifier.lemma_ == adjective:
                return True
    return False


def detect_dobj_intent(nlp: Language, doc: Doc) -> Optional[Intent]:
    obj = None
    dobj = get_dobj(doc)
    adjectives = get_adjectives(nlp, doc)

    if dobj:
        obj = get_delegated_intent_obj(dobj)
    elif adjectives:
        obj = adjectives[0][0]

    if obj and obj_has_adjective(obj, adjectives, 'cheap'):
        return Intent.CHEAPEST

    if obj and obj_has_adjective(obj, adjectives, 'expensive'):
        return Intent.MOST_EXPENSIVE

    return None


def detect_intent(nlp: Language, doc: Doc) -> Optional[Intent]:
    dobj_intent = detect_dobj_intent(nlp, doc)
    if dobj_intent:
        return dobj_intent

    advmod_filter = filter(lambda token: token.dep_ == 'advmod', list(doc))
    advmods = list(advmod_filter)
    if advmods and advmods[0].text.lower() == 'where':
        return Intent.CITY

    airport_filter = filter(lambda token: token.lemma_ == 'airport', list(doc))
    airports = list(airport_filter)
    if airports:
        return Intent.AIRPORT_CODE

    return None
