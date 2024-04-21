import re

pattern = re.compile(
    r"(?P<hostname>\S+)\s-\s- \[(?P<datetime>.*?)\] \"(?P<http_method>\S+)\s(?P<path>[^\"]+)(\sHTTP\/\d\.\d)?\"\s(?P<status_code>\d+)\s(?P<bytes>\d+)?"
)

#match.groupdict() -> lepiej by bylo

def extract_log(line: str):
    match = re.search(pattern, line)
    return match


if __name__ == "__main__":
    while True:
        try:
            log = input()
            match = extract_log(log)
            #print(match.group('datetime'))
        except AttributeError:
            print(log)
        except EOFError:
            break
