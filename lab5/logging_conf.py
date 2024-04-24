import logging
import sys
from utils import MessageType

formatter = logging.Formatter("%(levelname)s: %(message)s")
err_handler = logging.StreamHandler(sys.stderr)
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(formatter)
err_logger = logging.getLogger(__name__)
err_logger.addHandler(err_handler)
err_logger.propagate = False


def conf_root_logger(level):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    logging.basicConfig(
        level=level, handlers=[handler], format="%(levelname)s: %(message)s"
    )


def message_type_logging_handler(
    message_type: MessageType, username: str, event_description: str
) -> None:

    match message_type:
        case MessageType.SUCCESSFUL_LOG:
            logging.info(
                create_message(
                    f"{username} has successfully logged in.", event_description
                )
            )
        case MessageType.CONNECTION_CLOSED:
            logging.info(
                create_message(
                    f"{username} has successfully closed a session.", event_description
                )
            )
        case (
            MessageType.UNSUCCESSFUL_LOG
            | MessageType.INCORRECT_PASSWORD
            | MessageType.INCORRECT_USERNAME
        ):
            logging.warning(
                create_message(
                    f"{username} tried to log in but failed.", event_description
                )
            )
        case MessageType.ERROR:
            err_logger.error(create_message("Error has occured!", event_description))
        case MessageType.BREAK_IN_ATTEMPT:
            err_logger.critical(
                create_message(
                    f"{username} probably tried to break-in!!!", event_description
                )
            )
        case _:
            pass


def create_message(message: str, event_descr: str) -> str:
    return f"""{message}
        Event description: {event_descr}"""
