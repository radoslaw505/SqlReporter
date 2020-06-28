import sys
import os
import os.path
from os import listdir

from properties import REPORTS_PATH, SQL_PATH
from LoggerSetup import LoggerSetup

log = LoggerSetup().get_logger('SqlReporter')

class SqlReporter():

    def __init__(self):
        self.check_args()
        self.check_directory(REPORTS_PATH)
        self.check_directory(SQL_PATH)
        self.get_files(SQL_PATH)


    def get_files(self, path):
        log.debug('Calling get_files() method.')
        file_list = [f for f in listdir(path) if isfile(join(path, f))]
        print(file_list)


    def check_directory(self, path):
        log.debug('Calling check_directory() method for {}.'.format(path))
        if not os.path.exists(path):
            os.mkdir(path)
            log.info('Directory {} created.'.format(path))

    
    def check_args(self):
        if len(sys.argv) > 2:
            raise ValueError('You need to provide 0 or 1 arguments.\n\n\tUsage: {} [sql_file.sql]\n'.format(sys.argv[0]))


if __name__ == "__main__":
    reporter = SqlReporter()