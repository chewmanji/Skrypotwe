from lab2.util import extract_log
from typing import Match
from datetime import time, datetime


def extract_date(log: Match) -> datetime:
    log_time = log.group("datetime")
    d = datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S %z")
    return d


def is_within_period(check_time, start_time, end_time):
    if start_time > end_time:
        return (check_time >= start_time) or (check_time <= end_time)
    else:
        return start_time <= check_time <= end_time


if __name__ == "__main__":
    start = time(11)
    end = time(12)
    while True:
        try:
            log = input()
            match = extract_log(log)
            if match:
                time = extract_date(match).time()
                if is_within_period(time, start, end):
                    print(log)
        except EOFError:
            break
