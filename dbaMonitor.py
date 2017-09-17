#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import paramiko
import datetime
import osstatsENV
import generateHtml
import logEvent
import dbstatsENV
import osstats
import dbOper
import random
import re


#area_name_dict  = statsENV.area_name_dict
host_list       = osstatsENV.host_list
database_dict   = dbstatsENV.database_dict


day_label         = datetime.datetime.now().strftime('%Y-%m-%d')
time_label        = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#monitor_file_dir = os.getcwd()
monitor_file_base = 'D:\\coding\\python\\monitor2017090721'

log_file_dir      = os.path.join(monitor_file_base,datetime.datetime.now().strftime('%Y%m'))
html_file_dir     = os.path.join(monitor_file_base,'stats_file',datetime.datetime.now().strftime('%Y%m%d'))
#if not os.path.isdir(log_file_dir):
#    os.makedirs(log_file_dir)
if not os.path.isdir(html_file_dir):
    os.makedirs(html_file_dir)
log_file_name     = os.path.join(monitor_file_base,'log','stats_alert_' + datetime.datetime.now().strftime('%Y%m') +'.log')
logEvent.logEvent(log_file_name, logEvent.event_level[0],'开始巡检.....')
logEvent.logDelimiter(log_file_name, '='*100)

#每个月的5号、15号、25号生成html文件，其他时间只生成检查概要文件
is_generate_html = True
#if (datetime.datetime.now().strftime('%d')[-1]=='5'):
#    is_generate_html = True
#else:
#    is_generate_html = False

for i in range(len(host_list)):
#for i in range(3):
    username  = host_list[i][0]
    password  = host_list[i][1]
    area_code = str(host_list[i][5]).split('.')[1]
    area_name = host_list[i][3]
    #html_name = area_code.rjust(3,'0') + area_name + time_label + str(random.randint(11,99))+ '.html'
    html_name = area_code.rjust(3,'0') + area_name + time_label + '.html'
    stat_file_name_html = os.path.join(html_file_dir,html_name)

    #print(stat_fil e_name_html)
    if is_generate_html:
        html_file = open(stat_file_name_html,'a')
    
    
        html_file.write(generateHtml.getHtmlHeader())
        html_file.write(generateHtml.getHtmlTitle(area_code,area_name))
        html_file.write(generateHtml.getHtmlHeaderN(2,area_name,'系统统计信息',day_label))
   
    host_num = 1
    for ipaddr in host_list[i][5]:
        host_description = 'Node' + str(host_num)
        print((osstats.get_now() + '-' + ipaddr).center(80,"-"))
        #用来支持有些命令在linux和aix上格式不同
        if host_list[i][2] == '1':
            os_stat_list = osstatsENV.os_stat_list_linux
        elif host_list[i][2] == '2': 
            os_stat_list = osstatsENV.os_stat_list_aix
        conn = osstats.connect(ipaddr,username,password)
        
        for j in range(len(os_stat_list)):
            if is_generate_html:
                html_file.write(generateHtml.getHtmlHeaderN(3,'Node',str(host_num), ': ', os_stat_list[j][0] ,'统计信息'))
                html_file.write(generateHtml.getHtmlTableFromList(os_stat_list[j][2]))
            os_stat = osstats.get_system_stats(conn,os_stat_list[j][1])
            if is_generate_html:
                html_file.write(generateHtml.getHtmlTableFromList(os_stat,False))
            for oss in os_stat:
                osstats.llog(log_file_name, (area_name+ipaddr).ljust(30,' ')+os_stat_list[j][0], oss[0], oss[-1])
        #html_file.write('</html>')
        host_num = host_num + 1

    #数据库检查
    if host_list[i][4]:
        db_host      = host_list[i][5][0]
        db_list      = dbstatsENV.database_dict[db_host]
        for db_info in db_list:
            db_username  = db_info[0]
            db_password  = db_info[1]
            db_port      = db_info[2]
            db_name      = db_info[3]
            print(i)
            print(host_list[i][5][0])
            #是否检查数据库标记
            dbconnectoin = dbOper.get_conn(db_username,db_password,db_host,db_port,db_name)
            for db_stats_list in dbstatsENV.db_stat_list:
                #print(generateHtml.getHtmlHeaderN(3, db_stats_list[0]))
                if is_generate_html: 
                    html_file.write(generateHtml.getHtmlHeaderN(3, db_stats_list[0]))
                    #print(dbOper.get_column_name(dbconnectoin,db_stats_list[1]))
                    html_file.write(generateHtml.getHtmlTableFromList(dbOper.get_column_name(dbconnectoin,db_stats_list[1])))
                db_stat = dbOper.get_stats_result(dbconnectoin,db_stats_list[1])
                if is_generate_html: 
                    html_file.write(generateHtml.getHtmlTableFromList(db_stat,False))
                for dbs in db_stat:
                    if isinstance(dbs[0],int):
                        stats_name = str(dbs[0])
                    else:
                        stats_name = dbs[0]
                    dbOper.dblog(log_file_name,(area_name+db_host).ljust(30,' ') + db_stats_list[0], stats_name , dbs[-1],       db_stats_list[2]) #
            dbconnectoin.close()

    logEvent.logDelimiter(log_file_name, 'dedelimiter'.center(100,'-'))
    if is_generate_html:
        html_file.close()

 
mail_list = [r'xiepeiying@thtf.com.cn','wuhao@thtf.com.cn','wanghongchang@thtf.com.cn','leixaz@126.com']
#mail_list = [r'leixaz@126.com']
message = '严重警告信息：\n'
re_text   = '^' + datetime.datetime.now().strftime('%Y-%m-%d %H') + '.*' + 'CRITICAL' 
mo = re.compile(re_text)
with open(log_file_name, 'r') as f:
    for line in f.readlines():
        if mo.search(line):
            message = message + line
    print(message)
message = message + '重要警告信息：\n'
re_text   = '^' + datetime.datetime.now().strftime('%Y-%m-%d %H') + '.*' + 'MAJOR' 
mo = re.compile(re_text)
with open(log_file_name, 'r') as f:
    for line in f.readlines():
        if mo.search(line):
            message = message + line
    print(message)

message = message + '一般警告信息：\n'
re_text   = '^' + datetime.datetime.now().strftime('%Y-%m-%d %H') + '.*' + 'WARNING' 
mo = re.compile(re_text)
with open(log_file_name, 'r') as f:
    for line in f.readlines():
        if mo.search(line):
            message = message + line
    print(message)

message = message + '数据库记录警告信息：\n'
re_text   = '^' + datetime.datetime.now().strftime('%Y-%m-%d %H') + '.*' + 'Warning' 
mo = re.compile(re_text)
with open(log_file_name, 'r') as f:
    for line in f.readlines():
        if mo.search(line):
            message = message + line
    print(message)

mail_subject = datetime.datetime.now().strftime('%Y-%m-%d') + '数据库运行情况'
logEvent.send_mail(mail_subject,mail_list,message)