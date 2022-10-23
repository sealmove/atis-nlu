import json
from sqlite3 import Cursor
from spacy import Language
from atis.intent import *
from atis.entities import *


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
    if representation['intent'] == Intent.CHEAPEST.value:
        from_city = representation['entities']['locations']['from']
        dest_city = representation['entities']['locations']['to']
        c.execute('''
            select *, min(price)
            from flights as f, airports as a1, airports as a2
            where
                a1.city = ? collate nocase and
                a2.city = ? collate nocase and
                f.from_airport_code = a1.code and
                f.dest_airport_code = a2.code
        ''', [from_city, dest_city])
        rows = c.fetchall()
        print(rows)
        row = rows[0]
        return f'The cheapest flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'
    else:
        return 'Google it'
