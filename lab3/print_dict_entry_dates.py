from typing import Dict
from datetime import datetime



def print_dict_entry_dates(entries: Dict):
    #zalozenie: wpisy w liscie dla kazdego hosta są uporządkowane chronologicznie
    for host, requests in dict(list(entries.items())[:10]).items(): # tylko pierwszych 10 hostow
        _200s = sum(1  for r in requests if r["code"] == 200)

        print(
            f"""HOST : {host}
              Requests number: {len(requests)}
              First request: {datetime_to_str(requests[0]['datetime'])} | Last request: {datetime_to_str(requests[-1]['datetime'])}
              200 : others ratio: {_200s/len(requests)}"""
        )


def datetime_to_str(date:datetime):
    return date.strftime('%d/%m/%Y %H:%M:%S')