#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import paramiko
import datetime
#import statsENV
#import generateHtml
import logEvent




#filesystem_attr = statsENV.filesystem_attr
#cpu_attr        = statsENV.cpu_attr
#mem_attr        = statsENV.mem_attr
#area_name_dict  = statsENV.area_name_dict
#host_list       = statsENV.host_list
#database_dict   = statsENV.database_dict


def connect(host,username,password):  
    'this is use the paramiko connect the host,return conn'  
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    try:  
#       ssh.connect(host,username='root',allow_agent=True,look_for_keys=True) 
        if os.name == 'posix':
            key_file = '/Users/leixaz/.ssh/id_dsa'
        elif os.name == 'nt':
            key_file = 'D:\\Program Files\\cygwin64\\home\\Administrator\\.ssh\\id_dsa'
        ssh.connect(host,username=username,password=password,allow_agent=True,
                            key_filename=key_file) 
        return ssh  
    except Exception as err:
        print('connect error: ' + str(err))  
        return None  
  
def command(args,outpath):  
    'this is get the command the args to return the command'  
    cmd = '%s %s' % (outpath,args)  
    return cmd  
  
def exec_commands(conn,cmd):  
    'this is use the conn to excute the cmd and return the results of excute the command'  
    stdin,stdout,stderr = conn.exec_command(cmd) 
    results=stdout.readlines()  
    return results 
  
def excutor(host,outpath,args):  
    conn = connect(host)  
    if not conn:  
        return [host,None]  
    #exec_commands(conn,'chmod +x %s' % outpath)  
    cmd =command(args,outpath)  
    result = exec_commands(conn,cmd)  
    result = json.dumps(result)  
    return [host,result] 

def copy_module(conn,inpath,outpath):  
    'this is copy the module to the remote server'  
    ftp = conn.open_sftp()  
    ftp.put(inpath,outpath)  
    ftp.close()  
    return outpath  


def get_system_stats(conn,command):
    stats_command  = command
    stats_resultes = exec_commands(conn,command)
    for i in range(len(stats_resultes)):
        stats_resultes[i] = stats_resultes[i].strip().split(' ')   #把以","分隔的一维列表，转换为二维列表
    return stats_resultes

def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def llog(logfile_name, stats_tag, stats_name, stats_ratio, isdefault=True, *, named = ''):
    logfile = logfile_name
    if isdefault:
        if float(stats_ratio.strip('%')) >= 95:
            level = logEvent.event_level[3]
        elif float(stats_ratio.strip('%')) >= 80 and float(stats_ratio.strip('%')) < 95:
            level = logEvent.event_level[2]
        elif float(stats_ratio.strip('%')) >=70 and float(stats_ratio.strip('%')) < 80:
            level = logEvent.event_level[1]
        else:
            level = logEvent.event_level[0]
        message = stats_tag + ' "' + stats_name +'" ' + '使用率为' + stats_ratio + '.' 
        logEvent.logEvent(logfile, level,message)
