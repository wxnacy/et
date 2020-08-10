#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description: 发送邮件

import os
import sys
sys.path.append('{}/bin/py'.format(os.getenv("WS_HOME")))
import imaplib
import traceback
import argparse
import io
from email.header import decode_header
from email import message_from_string
from email.utils import parseaddr
from urllib.parse import urlparse
from config import ws_conf
import reprlib

class Email():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def connect_imap(self):
        imap_url = self.sec.folder
        url_config = urlparse(imap_url)
        conn = imaplib.IMAP4_SSL(host = url_config.hostname,
                port=url_config.port)
        print('已连接服务器')
        conn.login(self.sec['from'], self.sec.imap_pass)
        print('已登陆')
        self.imap_conn = conn

    def list_email(self):
        self.connect_imap()
        self.imap_conn.select()
        type, data = self.imap_conn.search(None, 'ALL')
        print(type, data)
        newlist=data[0].split()
        newlist.reverse()
        if not os.path.exists('/tmp/wshell/email'):
            os.makedirs('/tmp/wshell/email')
        print('sender\tsubject\tpath\tattachs')
        for nl in newlist:
            type, data = self.imap_conn.fetch(nl, '(RFC822)')
            msg = message_from_string(data[0][1].decode('utf-8'))
            result = parse_email_message(msg)
            #  print(result)
            result['subject'] = reprlib.repr(result['subject'])
            result['content'] = reprlib.repr(result['content'])
            print('{sender[0]}\t{subject}\t{content_path}\t{attachs}'.format(**result))

def decode_str(msg, name):
    '''解析字符串信息'''
    val = msg.get(name)
    value, charset = decode_header(val)[0]
    if charset:
        value = value.decode(charset)
    return value

def parse_email_message(msg):
    '''解析邮件信息'''
    subject = decode_str(msg, 'subject')
    sender = parseaddr(decode_str(msg, 'from'))
    to = parseaddr(msg.get("to"))
    content = None
    content_html = None
    content_path = None
    attachs = []
    for part in msg.walk():
        #  print(part.get_content_type(), part.is_multipart(), part.get_filename())
        #  if part.is_multipart():
            #  #  print(part.attach())
            #  print(part.get_filename())
            #  print(part.get_param("name"))
        if not part.is_multipart():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                content = part.get_payload(decode=True).decode('utf-8')
            elif content_type == 'text/html':
                content_html = part.get_payload(decode=True).decode('utf-8')
                content_path = '/tmp/wshell/email/{}.html'.format(str(hash(msg)))
                with open(content_path, 'w') as f:
                    f.write(content_html)
                    f.close()
        filename = part.get_filename()
        if filename:
            attachs.append(filename)

    result = dict(locals())
    result.pop('msg')
    result.pop('content_type')
    result.pop('part')
    return result

def init_args():
    '''初始化参数'''
    parser = argparse.ArgumentParser(description='Reveice email')
    parser.add_argument("emails",  help='Receive emails', nargs='+')
    parser.add_argument('-s', '--subject',  required=True, help='Email subject')
    parser.add_argument('-m', '--message',  help='Email content message')
    parser.add_argument('-a', '--attach',  help='Email attachments',
        action="append", default=[])

    return parser.parse_args()


if __name__ == '__main__':

    #  args = init_args()
    #  print(ws_conf.email)
    e = Email(ws_conf.email)
    e.list_email()
