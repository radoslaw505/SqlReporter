import sys
import os
import os.path
import cx_Oracle
import csv
from sys import exit
from os import listdir

from properties import REPORTS_PATH, SQL_PATH, headers, delimiter
from LoggerSetup import LoggerSetup
from oracle_config import user, passwd, host, port, sid

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
            self.execute_sql(sql_file, delimiter, REPORTS_PATH)
            
        else:
            log.warning('Chosen file {} is empty. The script ends.'.format(sql_file))
            sys.exit(1)


    def execute_sql(self, file, deli, path):
        log.debug('Calling oracle_insert() method.')
        try:
            dsn = cx_Oracle.makedsn(host, port, sid)
            conn = cx_Oracle.connect(
                user = user,
                password = passwd, 
                dsn = dsn
            )
            cur = conn.cursor()
            with open(file, 'r') as fp:
                sql = fp.read()
            cur.execute(sql)
            row = cur.fetchall()
            report_file = path + file.split('/')[-1].split('.')[0] + '.csv'
            with open(report_file, 'a', newline='') as report:
                a = csv.writer(report, delimiter=deli)
                a.writerows(row)
            log.info('Report generation for {} database completed.'.format(dsn))
        except Exception as ex:
            log.error('An error occured while connecting to database: {}'.format(ex), exc_info=True)
            sys.exit(1)
        finally:
            try:
                cur.close()
                conn.close()
            except NameError as nerr:
                pass


    def add_headers(self, header_check, headers):
        if header_check:
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