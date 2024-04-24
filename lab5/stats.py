from datetime import datetime
from ipaddress import IPv4Address
import random
import numpy as np
from statistics import mean, pstdev
from sys import maxsize
from utils import MessageType

USERS_ENTRIES: dict[str, list[dict]] = {}
USERS_IPS: dict[str, set[IPv4Address]] = {}
USERS_SESSIONS: dict[str, dict[int, tuple[datetime, datetime]]] = {}

def update_users_dict(username: str, log_dict: dict[str, str | int | datetime]) -> None:
    if username:
        if username in USERS_ENTRIES.keys():
            USERS_ENTRIES[username].append(log_dict)
        else:
            USERS_ENTRIES[username] = [log_dict]


def update_users_ips(username: str, ips: list[IPv4Address]) -> None:
    if username:
        if username not in USERS_IPS.keys():
            USERS_IPS[username] = set()

        for ip in ips:
            USERS_IPS[username].add(ip)


def random_entries_from_random_user():
    user = random.choice(list(USERS_ENTRIES.keys()))
    number_of_entries = random.randint(1, len(USERS_ENTRIES[user]) - 1)
    return np.random.choice(USERS_ENTRIES[user], number_of_entries)


def handle_update_user_session(
    username: str, mess_type: MessageType, log_dict: dict[str, str | int | datetime]
) -> None:
    match mess_type:
        case MessageType.SUCCESSFUL_LOG | MessageType.CONNECTION_CLOSED:
            pid = log_dict["PID"]
            timestamp = log_dict["datetime"]
            update_user_sessions(username, pid, timestamp)
        case _:
            return


def update_user_sessions(username: str, pid: int, time: datetime) -> None:
    if username not in USERS_SESSIONS.keys():
        USERS_SESSIONS[username] = {}

    if pid not in USERS_SESSIONS[username].keys():
        USERS_SESSIONS[username][pid] = (time, None)
    else:
        log_in_time = USERS_SESSIONS[username][pid][0]
        if log_in_time > time:
            time = time.replace(year=time.year + 1)
        USERS_SESSIONS[username][pid] = (log_in_time, time)


def calculate_all_durations() -> list[float]:
    durations: list[float] = []
    for sessions in USERS_SESSIONS.values():
        for t1, t2 in sessions.values():
            # t2 can be none because of lack of entry about closing session
            if t2:
                durations.append((t2 - t1).total_seconds())

    return durations


def global_mean() -> float:
    return mean(calculate_all_durations())


def global_stdev() -> float:
    return pstdev(calculate_all_durations())


def calculate_user_durations(username: str) -> list[float]:
    durations: list[float] = []
    for t1, t2 in USERS_SESSIONS[username].values():
        if t2:
            durations.append((t2 - t1).total_seconds())

    return durations


def user_mean(username: str) -> float:
    return mean(calculate_user_durations(username))


def user_stdev(username: str) -> float:
    return pstdev(calculate_user_durations(username))


def min_max_logging_users() -> tuple[tuple[str, int], tuple[str, int]]:
    min_user : tuple[str,int] = ("", maxsize)
    max_user : tuple[str,int] = ("", 0)
    for user, sessions in USERS_SESSIONS.items():
        number_of_logging = len(sessions)
        min_user = min(min_user, (user, number_of_logging), key=lambda x: x[1])
        max_user = max(max_user, (user, number_of_logging), key=lambda x: x[1])

    return (min_user, max_user)
