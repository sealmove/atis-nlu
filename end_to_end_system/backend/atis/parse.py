from spacy import Language
from atis.intent import *
from atis.entities import *
from atis.actions import *


def parse(nlp: Language, utterance: str) -> dict:
    doc = nlp(utterance)
    result = {}

    result['utterance'] = utterance

    intent = detect_intent(nlp, doc)
    if intent:
        result['intent'] = detect_intent(nlp, doc)

    result['entities'] = {}

    locations = extract_locations(nlp, doc)
    if locations:
        result['entities']['locations'] = locations

    airports = extract_airports(nlp, doc)
    if airports:
        result['entities']['airports'] = airports

    gpe_entity_filter = filter(lambda ent: ent.label_ == 'GPE', list(doc.ents))
    gpe_entities = list(gpe_entity_filter)
    if gpe_entities:
        gpe_entity_map = map(lambda ent: ent.text, gpe_entities)
        result['entities']['geopolitical'] = list(gpe_entity_map)

    return result
