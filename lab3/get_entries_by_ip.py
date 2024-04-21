from lab3.util import HOSTNAME
from typing import List, Tuple



def get_entries_by_ip(tuple_list: List[Tuple], address: str):
    try:
        result = [tup for tup in tuple_list if tup[HOSTNAME] == address]
    except KeyboardInterrupt:
        return result
    return result