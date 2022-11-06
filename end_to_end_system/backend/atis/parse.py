from spacy import Language
from atis.parse import *
from atis.intent import *
from atis.entities import *
from atis.actions import *


def parse(nlp: Language, utterance: str) -> str:
    doc = nlp(utterance)
    result = {}

    result['utterance'] = utterance

    intent = detect_intent(nlp, doc)
    if intent:
        print(f'{bcolors.OKGREEN}Detected intent:{bcolors.ENDC} {intent.value}')
        result['intent'] = detect_intent(nlp, doc)

    result['entities'] = {}

    locations = extract_locations(nlp, doc)
    if locations:
        result['entities']['locations'] = locations

    airports = extract_airports(nlp, doc)
    if airports:
        result['entities']['airports'] = airports
    return result
