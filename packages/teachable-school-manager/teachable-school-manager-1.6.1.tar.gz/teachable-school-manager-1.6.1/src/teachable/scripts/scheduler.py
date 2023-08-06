import schedule
import time
import subprocess
from ..api import Teachable
import os
from configparser import ConfigParser
import logging

api = Teachable()
# This is the template for all the scheduler fucntions we are going to run
# They are defined dynamically based on the scheduler.ini config file
func_template = '''def {}(): subprocess.run(["{}", "{}"]); return'''
main_func_template = '''schedule.every({}).{}{}.do({})'''


def get_config(configfile):
    """Gets config options"""
    logger = logging.getLogger(__name__)
    if os.path.exists(configfile):
        config = ConfigParser()
        config.read(configfile)
        logger.debug('Using config file {}'.format(configfile))
    else:
        config = None
        logger.error('Sorry no config file found at {}'.format(configfile))
    return config

logger = logging.getLogger(__name__)
conf_file = os.path.join(api.DEFAULT_DIRS['TEACHABLE_ETC_DIR'], 'scheduler.ini')
c = get_config(conf_file)


if c:
    for f in c.sections():
        logger.debug('defining function {}'.format(f))
        logger.debug(func_template.format(f,c[f]['script'],c[f]['opts']))
        exec(func_template.format(f,c[f]['script'],c[f]['opts']))


def main():
    # No config file no party
    logger = logging.getLogger(__name__)
    if c:
        for f in c.sections():
            logger.debug('Forking {}'.format(f))
            logger.debug(main_func_template.format(c[f]['every'], c[f]['when'],
                                                   '.at("' + c[f]['at_when'] + '")' if c[f]['at_when'] else '', f))
            exec(main_func_template.format(c[f]['every'], c[f]['when'],
                                           '.at("' + c[f]['at_when'] + '")' if c[f]['at_when'] else '', f))

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()
