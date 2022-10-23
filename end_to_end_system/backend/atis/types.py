from enum import Enum


class Intent(str, Enum):
    CHEAPEST = 'find_cheapest_flight'
    MOST_EXPENSIVE = 'find_most_expensive_flight'
    AIRPORT_CODE = 'find_airport_code'
    CITY = 'find_city_of_airport'
    FLIGHT = 'find_flight'
