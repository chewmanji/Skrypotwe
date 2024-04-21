from lab3.util import STATUS_CODE
from typing import List, Tuple

def get_entries_by_code(tuple_list: List[Tuple], code: int):
    try:
        result = [tup for tup in tuple_list if tup[STATUS_CODE] == code]
    except KeyboardInterrupt:
        return result
    return result