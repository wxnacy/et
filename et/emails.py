#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description: 邮件基础类

import os
import traceback
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class Email():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp = None

    def connect_smtp(self, smtp_host, smtp_port):
        '''创建 smtp 链接'''
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_host, smtp_port)
            smtp.login(self.email, self.password)
            self.smtp = smtp
        except smtplib.SMTPException as e:
            traceback.print_exc(e)

    def close_smtp(self):
        '''关闭 smtp 链接'''
        self.smtp.quit()

    def send(self, receivers,  subject, message=None, real_name=None, cc=[], attachs=[]):
        '''
        发送邮件
        '''
        msg = MIMEMultipart()
        sender_name = real_name or self.email
        msg['From'] = Header(sender_name, 'utf-8')
        msg['To'] = Header(','.join(receivers), 'utf-8')
        if cc:
            msg['Cc'] = Header(','.join(cc), 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        if message:
            msg.attach(MIMEText(message))

        for att in attachs:
            att1 = MIMEText(open(att, 'rb').read(), 'base64', 'utf-8')
            att1.add_header('Content-Disposition', 'attachment',
                filename=os.path.basename(att))
            msg.attach(att1)
        if cc:
            receivers.extend(cc)
        try:
            self.smtp.sendmail(self.email, receivers, msg.as_string())
            return True
        except Exception as e:
            traceback.format_exc(e)
            return False

email = Email('test@wxnacy.com', 'Test123456')

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    print(args)

    #  e = Email(ws_conf.email)
    #  e.list_email()

    e = Email(args[0], args[1])
    e.connect_smtp(args[2], args[3])
    e.send([args[4]], args[5])
    e.close_smtp()



