#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#logEvent.py

"""
event_level: MESSAGE, WARNING, MAJOR,CRITICAL
"""

import os
import datetime

#event_level = {'message':'MESSAGE','warning':'WARNING','major':'MAJOR','critical':'CRITICAL'}
event_level = ('MESSAGE','WARNING','MAJOR','CRITICAL')

def logEvent(logfile_name, level = '',log_message=''):
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile_dir = os.path.dirname(logfile_name)
    if not os.path.isdir(logfile_dir):
        os.mkdir(logfile_dir)
    logfile = open(logfile_name,'a')
    logfile.write(time_now + ': ' + level.rjust(8,' ') + ': ' + log_message + '\n')
    logfile.close()


def logDelimiter(logfile_name,string):
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile_dir = os.path.dirname(logfile_name)
    if not os.path.isdir(logfile_dir):
        os.mkdir(logfile_dir)
    logfile = open(logfile_name,'a')
    logfile.write(string+'\n')
    logfile.close()


def send_mail(v_header, *mail_info):
    from email import encoders
    from email.header import Header
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.utils import parseaddr, formataddr
    import smtplib
    import os
    

    mail_header = v_header
    print(mail_info)
    to_addr     = mail_info[0]   #list
    mail_text   = mail_info[1]   #str
    #if len (mail_info) == 3:
    #    attach_name = mail_info[2]   #name of the attach name str


    #def _format_addr(s):
    #    name, addr = parseaddr(s)
    #    return formataddr(( \
    #        Header(name, 'utf-8').encode(), \
    #        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _get_msg_to(to_addr_list):
        msg_to = ''
        for to_addr in to_addr_list:
            msg_to = msg_to + _format_addr(u'%s <%s>' %(to_addr.split('@')[0],to_addr)) + ','
        return msg_to
    
    from_addr = r'leixaz@126.com'
    smtp_server = r'smtp.126.com'
    
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' %(from_addr.split('@')[0],from_addr))
    msg['To'] = _get_msg_to(to_addr)
    msg['Subject'] = Header(mail_header, 'utf-8').encode()
    
    # 邮件正文是MIMEText:
    msg.attach(MIMEText(mail_text, 'plain', 'utf-8'))
    
    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    #if attach_name:
    #    with open(attach_name, 'rb') as f:
    #        # 设置附件的MIME和文件名:
    #        mime = MIMEBase('text', 'xls', filename='2015114_1327.xls')
    #        # 加上必要的头信息:
    #        mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_name))
    #        mime.add_header('Content-ID', '<0>')
    #        mime.add_header('X-Attachment-Id', '0')
    #        # 把附件的内容读进来:
    #        mime.set_payload(f.read())
    #        # 用Base64编码:
    #        encoders.encode_base64(mime)
    #        # 添加到MIMEMultipart:
    #        msg.attach(mime)
    
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(r'leixaz@126.com', r'shake.dog')
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

if __name__ == '__main__':
    for l in event_level:
        logfile_dir = os.getcwd()
        logfile = os.path.join(logfile_dir,'log','test.log')
        logEvent(logfile,l,'This is a ' + l +' test message.')