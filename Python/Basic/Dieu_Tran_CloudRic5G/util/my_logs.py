import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    from subprocess import run
    run('pip install coloredlogs'.split(),check=True)
    import coloredlogs
from os import makedirs
from os.path import isdir

logs:dict[str,logging.Logger] ={}

DEFAULT_LEVEL_STYLES = dict(
    spam=dict(color='green', faint=True),
    debug=dict(color='green'),
    verbose=dict(color='blue'),
    info=dict(),
    notice=dict(color='magenta'),
    warning=dict(color='yellow'),
    success=dict(color='green', bold=True),
    error=dict(color='red'),
    critical=dict(color='red', bold=True),
)

DEFAULT_FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color=25, bold=True),
    name=dict(color='blue'),
    programname=dict(color='cyan'),
    username=dict(color='yellow'),
    funcname=dict(color='blue',bright=True),
    filename=dict(color=207)
)

CONSOLE_FMT = '%(filename)s - %(funcName)s:%(lineno)d - %(levelname)8s - %(message)s'
FILE_FMT = f'%(asctime)8s,%(msecs)3d - {CONSOLE_FMT}'
# DATE_FMT = '%Y-%m-%d %H:%M:%S,'
DATE_FMT = '%H:%M:%S'
"""
----level number----
DEBUG: 10
INFO: 20
WARNING: 30
ERROR: 40
CRITICAL: 50

---- color board----
http://humanfriendly.readthedocs.io/en/latest/_images/ansi-demo.png
"""

def get_logger(log_name:str, 
               console_level = None, 
               file_level = None,
               console_format = None,
               file_format = None,
               file_mode = 'w',
               log_path='./logs') ->logging.Logger:
    if log_name not in logs:
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        if console_level is not None:
            if console_format:
                coloredlogs.DEFAULT_LOG_FORMAT = console_format
            else:
                coloredlogs.DEFAULT_LOG_FORMAT = CONSOLE_FMT
            coloredlogs.install(level=console_level, 
                                logger=log, 
                                level_styles = DEFAULT_LEVEL_STYLES, 
                                field_styles = DEFAULT_FIELD_STYLES)
        if file_level is not None:
            if not isdir(log_path):
                makedirs(log_path)
            f_handler = logging.FileHandler(f'{log_path}/{log_name}', mode=file_mode)
            f_handler.setLevel(file_level)
            if file_format:
                f_format = logging.Formatter(fmt = file_format,datefmt = DATE_FMT)
            else:
                f_format = logging.Formatter(fmt = FILE_FMT,datefmt = DATE_FMT)
            f_handler.setFormatter(f_format)
            log.addHandler(f_handler)
        logs[log_name] = log
    return logs[log_name]

if __name__ == "__main__":
    import time
    log = get_logger(log_name='test', console_level=logging.DEBUG, file_level=10)
    log.disabled = False
    log.debug('debug message')
    log.info('info message')
    time.sleep(0.5)
    log.warning('warn message')
    log.error('error message')
    log.critical('critical message')
