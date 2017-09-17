#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#generateHtml.py

"""
生成Html的文件头相关的
接收一维或二维的列表，然后后生成一个Html的Table
"""

import os

def getHtmlHeader():
    html_header = '<!DOCTYPE HTML><html lang="zh-cn"><head>\n'
    if os.name == 'posix':
        html_header = html_header + '<meta http-equiv="Content-Type" content="text/html; charset=utf8" />\n'
    elif os.name == 'nt':
        html_header = html_header + '<meta http-equiv="Content-Type" content="text/html; charset=gbk" />\n'
    html_header = html_header + '</head>\n'
    return html_header


def getHtmlTitle(*title):
    html_title = ''
    for t in title:
        html_title = html_title + t
    html_title = '<title>' + html_title + '</title>\n'
    html_title = html_title + '<html>\n'
    return html_title


def getHtmlHeaderN(n,*header):    
    html_headern = ''
    html_headern = '<h' + str(n) + '>'
    for h in header:
        html_headern = html_headern + h 
    html_headern = html_headern +  '</h' + str(n) + '>\n'
    return html_headern


def getHtmlTableFromList(table_list,is_table_header = True):
    html_table=''
    if is_table_header:
        html_table = '<table border="1" width="800">\n'
        html_table = html_table + '<tr><th>'
        if table_list == []:
            html_table = '</tr></th>'
        else:
            for t in table_list:
                html_table = html_table + t + '</th><th>'
            html_table = html_table[:-4] + '</tr>\n'
    elif not is_table_header:
        if table_list == []:
            html_table = ''
        else:
            if isinstance(table_list[0],list) or isinstance(table_list[0],tuple):
                html_table = '<tr><td>'
                for t in table_list:
                    for t1 in t:
                       html_table = html_table + str(t1) + '</td><td>'
                    html_table = html_table[:-4] + '</tr>\n<tr><td>'
                html_table  = html_table[:-9] +'\n'
            elif isinstance(table_list[0],str):
                html_table = "<tr><td>"
                for t in table_list:
                    html_table = html_table + str(t) + '</td><td>'  
                html_table = html_table[:-4] + '</tr>\n'

        html_table = html_table + '</table>\n'
    return html_table    


#test

if __name__ == '__main__':
    table_list_1 = ['100', '0', '0', '0']
    table_list_2 = [['MMMMM', 'NNNNNN', 'QQQQQQ', 'OOOOOOO'],['xxxxx', 'xxxxx', 'xxxxx', 'xxxx']]

    print(getHtmlFromList(table_list_2,False),end='')
