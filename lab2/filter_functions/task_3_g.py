from lab2.util import extract_log
from task_3_f import extract_date

if __name__ == "__main__":
    day = 4  # weekday as int, 0 -> monday ... 6 -> sunday
    while True:
        try:
            log = input()
            match = extract_log(log)
            if match:
                d = extract_date(match).weekday()
                if d == day:
                    print(log)
        except EOFError:
            break
