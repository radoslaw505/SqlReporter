import sys
import os
import os.path
import cx_Oracle
import csv
import time
from sys import exit
from os import listdir
from datetime import datetime

from properties import REPORTS_PATH, SQL_PATH, LOG_PATH, header_check, header, delimiter
from LoggerSetup import LoggerSetup
from oracle_config import user, passwd, host, port, sid


class SqlReporter():

    def __init__(self):
        self.log = LoggerSetup().get_logger('SqlReporter', LOG_PATH)

        self.check_args()
        self.check_directory(REPORTS_PATH)
        self.check_directory(SQL_PATH)


    def get_files(self, path):
        start_time = datetime.now()
        self.log.debug('Calling main method: get_files().')
        file_list = [f for f in listdir(path) if f.split('.')[-1] == 'sql']
        if len(sys.argv) == 2:
            if sys.argv[1] in file_list:
                sql_file = path + sys.argv[1]
            else:
                self.log.error('File {} not found in {} directory.'.format(sys.argv[1], path))
                sys.exit(1)
        else:
            self.log.info('Choose file from list to execute:')
            for count, sql in enumerate(file_list):
                print( '{0}) {1}'.format(count + 1, sql))
            try:
                value = input("Please enter a file number: ")
                self.log.info('You hase chosen: {}. Next step is to execute this query on database.'.format(file_list[int(value) - 1]))
                resume = input('Do you want to continue?[Y/n]: ')
                if resume != 'Y':
                    self.log.warning('You enter {}. Ending script.'.format(resume))
                    sys.exit(1)
                else:
                    sql_file = path + file_list[int(value) - 1]
            except Exception as ex:
                self.log.error("Invalid value for request: {ex}".format(ex), exc_info=True)
                sys.exit(1)
        if os.stat(sql_file).st_size != 0:
            self.execute_sql(sql_file, REPORTS_PATH, delimiter)
            self.add_headers(sql_file, REPORTS_PATH, header_check, header)    
        else:
            self.log.warning('Chosen file {} is empty. The script ends.'.format(sql_file.split('/')[-1]))
            sys.exit(1)
        self.log.info('Report generation is complete. Script duration: {}.'.format(datetime.now() - start_time))


    def execute_sql(self, file, path, delimiter):
        self.log.debug('Calling oracle_insert() method.')
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
                a = csv.writer(report, delimiter=delimiter)
                a.writerows(row)
            self.log.info('Report generation for {} database completed.'.format(dsn))
        except Exception as ex:
            self.log.error('An error occured while connecting to database: {}'.format(ex), exc_info=True)
            sys.exit(1)
        finally:
            try:
                cur.close()
                conn.close()
            except NameError as nerr:
                pass


    def add_headers(self, file, path, header_check, header):
        self.log.debug('Calling add_headers() method.')
        try:
            report_file = path + file.split('/')[-1].split('.')[0] + '.csv'
            if header_check:
                with open(report_file, 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
                    lines.insert(0, header)
                with open(report_file, 'w', newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                readFile.close()
                writeFile.close()
                self.log.info('Header has been added to report file: {}.'.format(report_file.split('/')[-1]))
            else:
                self.log.info('Header NOT added to report file: {}.'.format(report_file.split('/')[-1]))
            renamed_report = report_file.split('.')[0] + time.strftime("%Y%m%d-%H%M%S") + '.csv'
            os.rename(report_file, renamed_report)
        except Exception as ex:
            self.log.error('An error occured while executing add_headers() method: {}'.format(ex), exc_info=True)     


    def check_directory(self, path):
        self.log.debug('Calling check_directory() method for {}.'.format(path))
        if not os.path.exists(path):
            os.mkdir(path)
            self.log.info('Directory {} created.'.format(path))

    
    def check_args(self):
        if len(sys.argv) > 2:
            raise ValueError('You need to provide 0 or 1 arguments.\n\n\tUsage: {} [sql_file.sql]\n'.format(sys.argv[0]))


if __name__ == "__main__":
    reporter = SqlReporter()
    try:
        reporter.get_files(SQL_PATH)
    except Exception as ex:
        raise Exception(ex)
