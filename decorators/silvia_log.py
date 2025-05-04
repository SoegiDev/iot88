import logging
import functools
from flask import request
import json

def _generate_log(path,status = 0):
    """
    Create a logger object
    :param path: Path of the log file.
    :return: Logger object.
    """
    # Create a logger and set the level.
    
    logger = logging.getLogger('LogError')
    logger.setLevel(logging.ERROR)
    if status == 1:
        logger = logging.getLogger('LogSuccess')
        logger.setLevel(logging.INFO)
    if status == 2:
        logger = logging.getLogger('LogWarning')
        logger.setLevel(logging.WARNING)

    # Create file handler, log format and add the format to file handler
    file_handler = logging.FileHandler(path)
    

    # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    # for log format attributes.
    log_format = '%(levelname)s %(asctime)s %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(file_handler)
    # logger.handlers.clear()
    # logger.addHandler(file_handler)
    return logger


def add_log():
    """
    We create a parent function to take arguments
    :param path:
    :return:
    """
    from datetime import date
    path = "logs/silvia_info-" + str(date.today()) + ".log"
    def create_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Execute the called function, in this case `divide()`.
                # If it throws an error `Exception` will be called.
                # Otherwise it will be execute successfully.
                kwargs_params = None
                args_params = None
                codeOk = [200,201]
                if not kwargs:
                    if request.method == "POST" or request.method == "PATCH":                    
                        kwargs_params = json.loads(request.data)
                    else:
                        kwargs_params = kwargs
                else:
                    kwargs_params = kwargs
                    
                if not args:
                    if request.method == "GET":                    
                        args_params = args
                    else:
                       args_params = None
                else:
                    args_params = args
                results_function = func(*args,**kwargs)
                Hasil = results_function.data.decode("utf-8")
                values = f"Info -cls={func.__name__}|args={args_params}|kwargs={kwargs_params}|Result={Hasil}-"
                if results_function.status_code not in codeOk:
                    logger = _generate_log(path,2)
                    logger.warning(values)
                else:
                    logger = _generate_log(path,1)
                    logger.info(values)
                return results_function
            except Exception as e:
                logger = _generate_log(path,0)
                #error_msg = 'And error has occurred at /' + func.__name__ + '\n'
                error_msg = f"Error -cls={func.__name__}|Result={str(e)}|Exception={repr(e)}- \n"
                logger.exception(error_msg)
                return e  # Or whatever message you want.
        return wrapper
    return create_log