#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#exptab2csv.py

import os
import datetime
import dbaTools
import exptab2csvEnv



db_info_dict    = exptab2csvEnv.db_info_dict


def exptab2csv(isbgq):    
    dir_label     = datetime.datetime.now().strftime('%Y%m%d')
    csv_dir       = os.path.join(os.getcwd(), 'csv', dir_label)
    if not os.path.isdir(csv_dir):
        os.makedirs(csv_dir) 
    username    = db_info_dict['username']
    password    = db_info_dict['password']
    hostname    = db_info_dict['hostname']
    servicename = db_info_dict['servicename']
    port        = db_info_dict['port']
    if isbgq == 0:
        #生成csv文件名
        table_info_list = exptab2csvEnv.table_info_list_query
        for table_info in (table_info_list):
            tableowner    = table_info[0]
            tablename     = table_info[1]
            csv_name      = tablename + '.csv'
            csv_full_name = os.path.join(csv_dir, csv_name)
    
            query = table_info[2]
            dbaTools.export_to_csv(username,password,hostname,
                servicename,tableowner,tablename,csv_full_name,port,query)

    elif isbgq==1:
        table_info_list = exptab2csvEnv.table_info_list_bgq
        for table_info in (table_info_list):
            tableowner    = table_info[0]
            tablename     = table_info[1]
            csv_dir  =  os.path.join(os.getcwd(), 'csv', dir_label,tablename)
            if not os.path.isdir(csv_dir):
                os.makedirs(csv_dir)
            for bgq in table_info[2]:
                csv_name = 'BGQ_' + bgq + '.csv'
                csv_full_name = os.path.join(csv_dir, csv_name)
                query = "WHERE BGQ = '" + bgq + "'"
                dbaTools.export_to_csv(username,password,hostname,
                    servicename,tableowner,tablename,csv_full_name,port,query)

if __name__ == '__main__': 
    exptab2csv(1)