from typing import List, Tuple, Dict
from lab3.util import entry_to_dict, HOSTNAME

def log_to_dict(tuple_list: List[Tuple]) -> Dict:
    result = {}
    for tup in tuple_list:
        if tup[HOSTNAME] in result.keys():
            result[tup[HOSTNAME]].append(entry_to_dict(tup))
        else:
            result[tup[HOSTNAME]] = [entry_to_dict(tup)]

    return result