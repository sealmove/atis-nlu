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


def is_intent_cheapest(adjectives: list[tuple[Token, Token]], object: Token):
    for (target, modifier) in adjectives:
        if object == target:
            if modifier.lemma_ == 'cheap':
                return True
    return False


def is_intent_most_expensive(adjectives: list[tuple[Token, Token]], object: Token):
    for (target, modifier) in adjectives:
        if object == target:
            if modifier.lemma_ == 'expensive':
                return True
    return False


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

    if is_intent_cheapest(adjectives, intentObj):
        return Intent.CHEAPEST
    elif is_intent_most_expensive(adjectives, intentObj):
        return Intent.MOST_EXPENSIVE
