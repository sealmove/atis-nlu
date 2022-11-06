SQL_CHEAPEST_FROM_TO = '''
select *, min(price)
from flights as f, airports as a1, airports as a2
where
    a1.city = ? collate nocase and
    a2.city = ? collate nocase and
    f.from_airport_code = a1.code and
    f.dest_airport_code = a2.code
'''

SQL_CHEAPEST_FROM = '''
select *, min(price)
from flights as f, airports as a
where
    a.city = ? collate nocase and
    f.from_airport_code = a.code
'''

SQL_CHEAPEST_TO = '''
select *, min(price)
from flights as f, airports as a
where
    a.city = ? collate nocase and
    f.dest_airport_code = a.code
'''

SQL_MOST_EXPENSIVE_FROM_TO = '''
select *, max(price)
from flights as f, airports as a1, airports as a2
where
    a1.city = ? collate nocase and
    a2.city = ? collate nocase and
    f.from_airport_code = a1.code and
    f.dest_airport_code = a2.code
'''

SQL_MOST_EXPENSIVE_FROM = '''
select *, max(price)
from flights as f, airports as a
where
    a.city = ? collate nocase and
    f.from_airport_code = a.code
'''

SQL_MOST_EXPENSIVE_TO = '''
select *, max(price)
from flights as f, airports as a
where
    a.city = ? collate nocase and
    f.dest_airport_code = a.code
'''

SQL_CITY_OF_AIRPORT = '''
select city
from airports as a
where a.code = ? collate nocase
'''

SQL_AIRPORT_CODE_OF_CITY = '''
select code
from airports as a
where a.city = ? collate nocase
'''
