from sqlite3 import Cursor
from atis.types import *


def action_cheapest(c: Cursor, representation: dict) -> str:
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


def action_most_expensive(c: Cursor, representation: dict) -> str:
    from_city = representation['entities']['locations']['from']
    dest_city = representation['entities']['locations']['to']
    c.execute('''
        select *, max(price)
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
    return f'The most expensive flight from {row[0]} to {row[1]} is at {row[2]} and costs ${row[3]}'


def action(c: Cursor, representation: dict) -> str:
    if representation['intent'] == Intent.CHEAPEST.value:
        return action_cheapest(c, representation)
    elif representation['intent'] == Intent.MOST_EXPENSIVE.value:
        return action_most_expensive(c, representation)
    else:
        return 'Google it'
