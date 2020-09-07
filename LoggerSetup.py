import logging
import time
import os
import os.path


class LoggerSetup():
    def get_logger(self, ctrl_file, path):
        if not os.path.exists(path):
            os.mkdir(path)
        control_file = path + ctrl_file + time.strftime("%Y%m%d-%H%M%S") + '.log'
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