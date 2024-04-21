from typing import List, Tuple, Match, Dict

from lab2.filter_functions.task_3_f import extract_date
from lab2.filter_functions.task_3_h import extract_hostname
from lab2.reduction_functions.task_3_b import extract_resource_size
from lab2.reduction_functions.task_3_c import extract_path_to_resource


# indexes in tuple
HOSTNAME = 0
DATETIME = 1
METHOD = 2
RESOURCE_PATH = 3
STATUS_CODE = 4
RESOURCE_SIZE = 5


def extract_status_code(match: Match):
    return int(match.group("status_code"))


def create_tuple(match: Match):
    hostname = extract_hostname(match)
    datetime = extract_date(match)
    method = match.group("http_method")
    resource_path = extract_path_to_resource(match)
    status_code = extract_status_code(match)
    resource_size = extract_resource_size(match)
    return (hostname, datetime, method, resource_path, status_code, resource_size)


def entry_to_dict(tup: Tuple):
    return {
        "hostname": tup[HOSTNAME],
        "datetime": tup[DATETIME],
        "method": tup[METHOD],
        "path": tup[RESOURCE_PATH],
        "code": tup[STATUS_CODE],
        "size": tup[RESOURCE_SIZE],
    }


def get_addrs(entries: Dict):
    return list(entries.keys())


def print_entries(tuple_list: List[Tuple]):
    for tup in tuple_list:
        print(
            f"HOSTNAME / IP: {tup[HOSTNAME]} | TIME: {tup[DATETIME]} | HTTP method: {tup[METHOD]} | PATH: {tup[RESOURCE_PATH]} | STATUS CODE: {tup[STATUS_CODE]} | SIZE: {tup[RESOURCE_SIZE]}B"
        )


def print_dict_entry_dates(entries: Dict):
    pass
