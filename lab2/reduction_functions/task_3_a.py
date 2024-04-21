from typing import Match
from lab2.util import extract_log


def check_status_code(log: Match, statuscode: int) -> int:
    if log:
        return 1 if int(log.group("status_code")) == statuscode else 0
    return 0

def main(statuscode:int):
    result = 0
    while True:
        try:
            log = input()
            match = extract_log(log)
            result += check_status_code(match, statuscode)
        except EOFError:
            print(f'{result} requests with status code : {statuscode}')
            break
