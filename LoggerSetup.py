import logging
import time
import os
import os.path

from properties import LOG_PATH

class LoggerSetup():
    def get_logger(self, ctrl_file):
        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)
        control_file = LOG_PATH + ctrl_file + time.strftime("%Y%m%d-%H%M%S") + '.log'
        log = logging.getLogger('log')
        logging.basicConfig(
            format='[%(asctime)s][%(process)-6s][%(levelname)-7s]: %(message)s',
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(control_file),
                logging.StreamHandler()
                ]
        )
        log.info('Logging has been set up. Control file: {}'.format(control_file))
        return log