import logging as log

log.basicConfig(
    filename="logs.txt",
    filemode='a',
    level=log.INFO,
)

def log_info(*message) -> None:
    log.info(20*'-')
    log.info(message)
    log.info(20*'-')