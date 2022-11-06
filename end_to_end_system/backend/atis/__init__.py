import json
from sqlite3 import Cursor
from spacy import Language
from atis.parse import *
from atis.intent import *
from atis.entities import *
from atis.actions import *
from atis.debug import bcolors


def answer(c: Cursor, nlp: Language, utterance: str) -> str:
    representation = parse(nlp, utterance)
    print(bcolors.OKCYAN, end='')
    print(json.dumps(representation, indent=4))
    print(bcolors.ENDC, end='', flush=True)
    if 'intent' in representation:
        return action(c, representation)
    else:
        print(f'{bcolors.FAIL}No intent detected{bcolors.ENDC}')
        return 'Google it'
