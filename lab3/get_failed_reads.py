from lab3.util import STATUS_CODE
from typing import List, Tuple


def get_failed_reads(tuple_list: List[Tuple], to_merge: bool = True):
    _4xx_list = []
    _5xx_list = []

    # tu nie ma sensu sie bawic w onelinery, list comprehensions, ternary operators bo trzeba by bylo iterowac dwa razy (CHYBA)
    for tup in tuple_list:
        status_code = tup[STATUS_CODE]
        if status_code >= 400:
            if status_code < 500:
                _4xx_list.append(tup)
            else:
                _5xx_list.append(tup)

    if to_merge:
        return _4xx_list + _5xx_list  # Combine lists for single output (if desired)
    else:
        return _4xx_list, _5xx_list