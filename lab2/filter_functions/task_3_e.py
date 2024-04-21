from lab2.util import extract_log
from lab2.reduction_functions.task_3_a import check_status_code


if __name__ == "__main__":
    while True:
        try:
            log = input()
            match = extract_log(log)
            if bool(check_status_code(match, statuscode=200)):
                print(log)
        except EOFError:
            break