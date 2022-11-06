from sqlite3 import Cursor, Row
from typing import Optional
from atis.types import *
from atis.debug import bcolors
from atis.queries import *


def fetch_row(c: Cursor) -> Optional[Row]:
    rows = c.fetchall()
    if rows:
        print(f"{bcolors.OKGREEN}Matched rows:{bcolors.ENDC}")
        for row in rows:
            print("\t", end='')
            print(row)
        row = rows[0]
        if all(e is None for e in row):
            return None
        return row
    else:
        print(f"{bcolors.FAIL}No match{bcolors.ENDC}")
        return None


def action_cheapest(c: Cursor, representation: dict) -> str:
    from_city = representation['entities']['locations'].get('from')
    dest_city = representation['entities']['locations'].get('to')
    if from_city and dest_city:
        c.execute(SQL_CHEAPEST_FROM_TO, [from_city, dest_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The cheapest flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'
    elif from_city:
        c.execute(SQL_CHEAPEST_FROM, [from_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The cheapest flight from {row[0]} is towards {row[1]}, at {row[2]} and costs ${row[3]}'
    elif dest_city:
        c.execute(SQL_CHEAPEST_TO, [dest_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The cheapest flight towards {row[1]} is from {row[0]} at {row[2]} and costs ${row[3]}'
    else:
        print(f"{bcolors.FAIL}Not enough location entities detected{bcolors.ENDC}")
        return 'Google it'


def action_most_expensive(c: Cursor, representation: dict) -> str:
    from_city = representation['entities']['locations'].get('from')
    dest_city = representation['entities']['locations'].get('to')
    if from_city and dest_city:
        c.execute(SQL_MOST_EXPENSIVE_FROM_TO, [from_city, dest_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The most expensive flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'
    elif from_city:
        c.execute(SQL_MOST_EXPENSIVE_FROM, [from_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The most expensive flight from {row[0]} is towards {row[1]}, at {row[2]} and costs ${row[3]}'
    elif dest_city:
        c.execute(SQL_MOST_EXPENSIVE_TO, [dest_city])
        row = fetch_row(c)
        if not row:
            return 'No flights found'
        return f'The most expensive flight towards {row[1]} is from {row[0]} at {row[2]} and costs ${row[3]}'
    else:
        print(f"{bcolors.FAIL}Not enough location entities detected{bcolors.ENDC}")
        return 'Google it'


def action_city(c: Cursor, representation: dict) -> str:
    airports = representation['entities'].get('airports')
    if not airports or len(airports) == 0:
        print(f"{bcolors.FAIL}Not airport entity detected{bcolors.ENDC}")
        return 'Google it'
    c.execute(SQL_CITY_OF_AIRPORT, [airports[0]])
    row = fetch_row(c)
    if not row:
        return 'Airport not found'
    return f'{airports[0]} is in {row[0]}'


def action(c: Cursor, representation: dict) -> str:
    if representation['intent'] == Intent.CHEAPEST.value:
        return action_cheapest(c, representation)
    elif representation['intent'] == Intent.MOST_EXPENSIVE.value:
        return action_most_expensive(c, representation)
    elif representation['intent'] == Intent.CITY.value:
        return action_city(c, representation)
    else:
        return 'Not implemented yet'
