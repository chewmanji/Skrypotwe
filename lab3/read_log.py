from typing import List, Tuple
from lab2.util import extract_log
from lab3.util import create_tuple

def read_log() -> List[Tuple]:
    result_list = []
    while True:
        try:
            log = input()
            match = extract_log(log)
            if match:
                #print(match.groupdict())
                t = create_tuple(match)
                result_list.append(t)
        except EOFError:
            return result_list
        
if __name__ == "main":
    read_log()