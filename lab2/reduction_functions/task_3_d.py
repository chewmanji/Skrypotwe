from lab2.util import extract_log
from task_3_b import extract_resource_size
from task_3_c import extract_path_to_resource

EXTENSIONS = []
if __name__ == "__main__":
    graphics = 0
    other = 0
    while True:
        try:
            log = input()
            match = extract_log(log)
            size = extract_resource_size(match)
            path = extract_path_to_resource(match)
            if path.endswith((".gif", ".jpg", ".jpeg", ".xbm")):
                graphics += size
            else:
                other += size

        except EOFError:
            print(
                f"Downloaded graphics data is {graphics/(1024**3)} GB and other data is {other/(1024**3)} GB\nTheir ratio is 1 : {round(other/(graphics if graphics != 0 else 1), 2)}"
            )
            break
