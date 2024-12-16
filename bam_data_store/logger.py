import copy

import structlog

# List to store log messages
log_storage = []


def store_log_message(_, __, event_dict):
    """
    Custom processor to store log messages in a list of dictionaries containing the log messages as:

        {
            'event': <the log message>,
            'timestamp': <the timestamp>,
            'level': <the log level (info, debug, warning, etc)>,
        }
    """
    log_storage.append(copy.deepcopy(event_dict))
    return event_dict


# Configure structlog with the custom processor
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.add_log_level,
        store_log_message,
        structlog.dev.ConsoleRenderer(),
    ],
)

# Create a logger instance
logger = structlog.get_logger()
