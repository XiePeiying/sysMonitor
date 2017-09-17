#!/usr/bin/env  python3
# -*- coding: utf-8 -*-

#!dbaTools.py


import cx_Oracle
import logEvent
import csv
import sys
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


import dbOper

def export_to_csv(username,password,hostname,service_name,table_owner,table_name,csvfile_name,port = '1521',query = ''):
    sql    = ''
    conn   = dbOper.get_conn(username,password,hostname,port,dbname=service_name)
    cursor = conn.cursor()
    sql    = 'SELECT * FROM ' + table_owner + '.' + table_name + ' ' + query
    csv_file = open(csvfile_name,'w',encoding='utf-8')
    writer   = csv.writer(csv_file,lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    cursor.execute("alter session set nls_date_format = 'yyyy-mm-dd hh24:mi:ss' ")
    cursor.execute(sql)
    for row in cursor:
        writer.writerow(row)
    csv_file.close()
    print(('Exporting table ' + table_owner + '.' + table_name + ' ' + query).ljust(100,'.') 
    	+ (str(cursor.rowcount) + ' rows ').rjust(20,'.'))
    cursor.close()
    conn.close()


if __name__ == '__main__':
    export_to_csv('scott','tiger','192.168.1.112','testdb1','scott','emp')



#import csv
#import cx_Oracle
#db = cx_Oracle.connect('hr/hrpwd@localhost:1521/XE')
#cursor = db.cursor()
#f = open("job_history.csv", "w")
#writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)
#r = cursor.execute(" "SELECT * FROM job_history ORDER BY employee_id, start_date")
#for row in cursor:
#  writer.writerow(row)
#
#f.close()
#
