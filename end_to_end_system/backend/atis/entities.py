from spacy import Language
from spacy.tokens import Doc
from spacy.matcher import Matcher


def extract_locations(nlp: Language, doc: Doc) -> dict:
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'ADP', 'OP': '+'}, {'ENT_TYPE': 'GPE', 'OP': '+'}]
    matcher.add('Location', [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    locations = {s[0].text: s[1:].text for s in spans}
    return locations


def extract_airports(nlp: Language, doc: Doc) -> dict:
    matcher = Matcher(nlp.vocab)
    pattern = [{'TEXT': {'REGEX': '[A-Z]{3}'}}]
    matcher.add('Airports', [pattern])
    matches = matcher(doc)
    airports = [doc[start:end].text for _, start, end in matches]
    return airports
