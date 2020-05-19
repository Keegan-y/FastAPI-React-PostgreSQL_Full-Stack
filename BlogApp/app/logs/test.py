import sys

sys.path.append("..")
from logs.logutil_file import fastapi_logger


def check_log():
    try:
        1 / 0
    except ZeroDivisionError:
        fastapi_logger.exception(1)


if __name__ == "__main__":
    check_log()
