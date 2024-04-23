from pathlib import Path
import argparse
from extract import get_user_from_log, get_message_type
from utils import read_log_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", required=True)
    args = parser.parse_args()

    # mTypes = {
    #     MessageType.SUCCESSFUL_LOG: 0,
    #     MessageType.UNSUCCESSFUL_LOG: 0,
    #     MessageType.CONNECTION_CLOSED: 0,
    #     MessageType.INCORRECT_PASSWORD: 0,
    #     MessageType.INCORRECT_USERNAME: 0,
    #     MessageType.BREAK_IN_ATTEMPT: 0,
    #     MessageType.OTHER: 0
    # }

    for x in read_log_file(Path(args.path)):
        get_message_type(x)
        
   

    # for key, value in mTypes.items():
    #     print(f"Message type: {key}, Count: {value}")

    # print(f"Sum: {sum(mTypes.values())}")