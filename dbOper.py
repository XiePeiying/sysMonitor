#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#dbOper.py


import cx_Oracle
import logEvent
import csv


def get_conn(username,password,hostname,port,dbname):
    dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=dbname)
    try:
        conn = cx_Oracle.connect(username,password,dsn_tns)
        return conn
    except Exception as err:
        print(str(err))


def get_column_name(conn,sql):
    cur = conn.cursor()
    column_name_list = []
    cur.execute(sql)
    for column in cur.description:
        column_name_list.append(column[0])
    cur.close()
    return column_name_list


def get_stats_result(conn,sql):
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result


def get_table_result(table_owner, table_name,conn):
    cur = conn.cursor()
    sql = 'SELECT * FROM ' + table_owner + '.' + table_name
    cur.execute(sql)


    #写出行到


def dblog(logfile_name, stats_tag, stats_name, stats_ratio=0, isnumber=True, *, named = ''):
    logfile = logfile_name
    if isnumber:
        if stats_ratio >= 95:
            level = logEvent.event_level[3]
        elif stats_ratio >= 80 and stats_ratio < 95:
            level = logEvent.event_level[2]
        elif stats_ratio >=70 and stats_ratio < 80:
            level = logEvent.event_level[1]
        else:
            level = logEvent.event_level[0]
        message = stats_tag + ' "' + stats_name +'" ' + '使用率为' + str(stats_ratio) + '.' 
        logEvent.logEvent(logfile, level,message)
    elif not isnumber:
        level = logEvent.event_level[0]
        message = 'Check ' + stats_tag + ' "' + stats_name +'" ' +  ' information.'
        logEvent.logEvent(logfile, level, message)


if __name__ == '__main__':
    username = 'cjcl'
    password = 'cjclpassword'
    hostname = '192.168.1.112'
    port     = '1521'
    dbname   = 'snpcjdb'
    sql      = 'select * from dba_users'
    connect = get_conn(username,password,hostname,port,dbname)

    #for i
    #print(get_stat_result(cur,sql))
    print(get_column_name(connect,sql))
    print(get_stat_result(connect,sql))