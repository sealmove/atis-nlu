from sqlite3 import Cursor, Row
from typing import Optional
from atis.types import *
from atis.debug import bcolors
from atis.queries import *


def fetch_rows(c: Cursor) -> Optional[Row]:
    rows = c.fetchall()
    if rows:
        print(f"{bcolors.OKGREEN}Matched rows:{bcolors.ENDC}")
        for row in rows:
            print("\t", end='')
            print(row)
        row = rows[0]
        if all(e is None for e in row):
            return None
        return rows
    else:
        print(f"{bcolors.FAIL}No match{bcolors.ENDC}")
        return None


def action_cheapest(c: Cursor, representation: dict) -> str:
    from_city = representation['entities']['locations'].get('from')
    dest_city = representation['entities']['locations'].get('to')
    if from_city and dest_city:
        c.execute(SQL_CHEAPEST_FROM_TO, [from_city, dest_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The cheapest flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'
    elif from_city:
        c.execute(SQL_CHEAPEST_FROM, [from_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The cheapest flight from {row[0]} is towards {row[1]}, at {row[2]} and costs ${row[3]}'
    elif dest_city:
        c.execute(SQL_CHEAPEST_TO, [dest_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The cheapest flight towards {row[1]} is from {row[0]} at {row[2]} and costs ${row[3]}'
    else:
        print(f"{bcolors.FAIL}Not enough location entities detected{bcolors.ENDC}")
        return 'Google it'


def action_most_expensive(c: Cursor, representation: dict) -> str:
    from_city = representation['entities']['locations'].get('from')
    dest_city = representation['entities']['locations'].get('to')
    if from_city and dest_city:
        c.execute(SQL_MOST_EXPENSIVE_FROM_TO, [from_city, dest_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The most expensive flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'
    elif from_city:
        c.execute(SQL_MOST_EXPENSIVE_FROM, [from_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The most expensive flight from {row[0]} is towards {row[1]}, at {row[2]} and costs ${row[3]}'
    elif dest_city:
        c.execute(SQL_MOST_EXPENSIVE_TO, [dest_city])
        rows = fetch_rows(c)
        if not rows:
            return 'No flights found'
        row = rows[0]
        return f'The most expensive flight towards {row[1]} is from {row[0]} at {row[2]} and costs ${row[3]}'
    else:
        print(f"{bcolors.FAIL}Not enough location entities detected{bcolors.ENDC}")
        return 'Google it'


def action_city(c: Cursor, representation: dict) -> str:
    airports = representation['entities'].get('airports')
    if not airports or len(airports) == 0:
        print(f"{bcolors.FAIL}No airport entity detected{bcolors.ENDC}")
        return 'Google it'
    c.execute(SQL_CITY_OF_AIRPORT, [airports[0]])
    rows = fetch_rows(c)
    if not rows:
        return 'Airport not found'
    row = rows[0]
    return f'{airports[0]} is in {row[0]}'


def action_airport_code(c: Cursor, representation: dict) -> str:
    if 'geopolitical' not in representation['entities'] or not representation['entities']['geopolitical']:
        print(f"{bcolors.FAIL}Did not recognise intented city of airport{bcolors.ENDC}")
        return 'Google it'
    city = representation['entities']['geopolitical'][0]
    c.execute(SQL_AIRPORT_CODE_OF_CITY, [city])
    rows = fetch_rows(c)
    if not rows:
        return 'Airport not found'
    airports = list(map(lambda row: row[0], rows))
    return f'The airports of {city} are ' + ', '.join(airports)


def action(c: Cursor, representation: dict) -> str:
    intent = representation['intent']
    if intent == Intent.CHEAPEST.value:
        return action_cheapest(c, representation)
    elif intent == Intent.MOST_EXPENSIVE.value:
        return action_most_expensive(c, representation)
    elif intent == Intent.CITY.value:
        return action_city(c, representation)
    elif intent == Intent.AIRPORT_CODE.value:
        return action_airport_code(c, representation)
    else:
        return 'Not implemented yet'
