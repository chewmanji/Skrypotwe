from typing import Match
from lab2.util import extract_log


def extract_hostname(log: Match) -> str:
    return log.group("hostname")


if __name__ == "__main__":
    while True:
        try:
            log = input()
            match = extract_log(log)
            if match:
                name = extract_hostname(match)
                if name.endswith(".pl"):
                    print(log)
        except EOFError:
            break
