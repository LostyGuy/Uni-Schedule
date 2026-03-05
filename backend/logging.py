import logging as log
import inspect

log.basicConfig(
    filename="logs.txt",
    filemode='a',
    level=log.INFO,
)

def log_info(*message) -> None:
    log.info(20*'-')
    log.info(message)
    log.info(20*'-')
    
def log_info_test_space(*message) -> None:
    log.info(20*'-')
    log.info('Testing Space')
    log.info(message)
    log.info(20*'-')
    
current_function = inspect.currentframe().f_code.co_name