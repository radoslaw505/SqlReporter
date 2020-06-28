import sys
import os
import os.path
from sys import exit
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
        file_list = [f for f in listdir(path) if f.split('.')[-1] == 'sql']
        if len(sys.argv) == 2:
            if sys.argv[1] in file_list:
                sql_file = path + sys.argv[1]
        else:
            log.info('Choose file from list to execute:')
            for count, sql in enumerate(file_list):
                print( '{0}) {1}'.format(count + 1, sql))
            try:
                value = input("Please enter a file number: ")
                log.info('You hase chosen: {}. Next step is to execute this query on database.'.format(file_list[int(value) - 1]))
                resume = input('Do you want to continue?[Y/n]: ')
                if resume != 'Y':
                    log.info('You enter {}. Ending script.'.format(resume))
                    sys.exit(1)
                else:
                    sql_file = path + file_list[int(value) - 1]
            except Exception as ex:
                log.error("Invalid value for request. The script ends.", exc_info=True)
                sys.exit(1)
        if os.stat(sql_file).st_size != 0:
            self.execute_sql(sql_file)
        else:
            log.warning('Chosen file {} is empty. The script ends.'.format(sql_file))
            sys.exit(1)


    def execute_sql(self, file):
        pass


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