import logging
def log_msg(level, *message):

    _msg = " ".join(message)
    print(
        f"[{level}] ", _msg
    )
