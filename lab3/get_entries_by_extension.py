from lab3.util import RESOURCE_PATH
from typing import List, Tuple

def get_entries_by_extension(tuple_list: List[Tuple], extension: str):
    try:
        result = [tup for tup in tuple_list if tup[RESOURCE_PATH].endswith(extension)]
    except KeyboardInterrupt:
        return result
    return result