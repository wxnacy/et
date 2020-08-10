#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import logging
import logging.handlers


def create_logger():
    """创建日志"""

    logger = logging.getLogger('tmdapi')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(
        '/tmp/et.log', maxBytes=104857600, backupCount=20
    )
    #  error_file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    return logger

logger = create_logger()

import time

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Box, Button, Frame, TextArea
from wcwidth import wcswidth
#  from et import Email
from et import email

buffer1 = Buffer()  # Editable buffer.

from prompt_toolkit.shortcuts import button_dialog


def create_dialog():
    return button_dialog(
        title='Button dialog example',
        text='Are you sure?',
        buttons=[
            ('Yes', True),
            ('No', False),
            ('Maybe...', None),
        ],
    ).run()


emails = {
    "1": Window(content=FormattedTextControl(text='1 Hello world'), height=1),
    "2": Window(content=FormattedTextControl(text='2 Hello world'), height=1),
    "3": Window(content=FormattedTextControl(text='3 Hello world'), height=1),
}

revs = Box(
    Frame(TextArea(
        text='Hello world',
        width=40,
        height=1,
    )),
)

email_list = [v for k, v in emails.items()]

def create_input(name, label, default=''):
    return HSplit([
        #  Window(height=1, char='-'),
        VSplit([
            Window(content=FormattedTextControl(text=label), height=1,
                width=wcswidth(label)+1),
            Window(content=BufferControl(buffer=Buffer(name=name)), height=1),
        ]),
        Window(height=1, char='-'),
    ])

def get_text_by_name(app, name):
    return app.layout.get_buffer_by_name(name).text

status_control =FormattedTextControl(text='status')
status=Window(status_control, height=1)

def send_email():
    receivers = get_text_by_name(application, 'receivers')
    subject = get_text_by_name(application, 'subject')
    content = get_text_by_name(application, '')
    #  waiting.text = 'waiting'
    #  logger.debug(status.content = 'test')
    #  status = Window(FormattedTextControl(text='test'))
    #  status_control.text = 'waiting'
    #  wait_app = Application(layout=Layout(Box(Frame(TextArea(text='waint')))), full_screen=True)
    #  wait_app.run()
    #  time.sleep(1)
    #  email.connect_smtp('smtp.qiye.aliyun.com', 25)
    #  email.send([receivers], subject, content)
    #  email.close_smtp()
    #  waiting.text = ''
    #  status_control.text = ''
    #  wait_app.exit()
    #  application.layout = Layout(Box(Frame(TextArea(text='waiting'))))
    application.exit()
    create_dialog()
    logger.debug(dir(application))

waiting = FormattedTextControl(text='')
send_btn = Button('发送', handler=send_email, width=30)
buttons = VSplit([
    send_btn,
    Window(waiting, width=10)
])


body = HSplit([
    create_input('receivers', '接收人'),
    create_input('subject', '主题'),
    Window(FormattedTextControl(text='内容'), height=1),
    Frame(TextArea(
        text='\n--------------------\nSend email by et',
    )),
    buttons,
    #  status_control
    status
])

kb = KeyBindings()

@kb.add('q')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

@kb.add('tab')
def _(event):
    logger.debug(event.app.layout)
    logger.debug(dir(event.app.layout))
    logger.debug(event.app.layout.current_buffer)
    logger.debug(event)
    event.app.layout.focus_next()

def get_key(event):
    '''获取按下的 key'''
    return event.app.key_processor.key_buffer[0].key

@kb.add('b')
def _(event):
    key = get_key(event)
    #  logger.debug(dir(event.app))
    #  logger.debug(event.app.key_processor)
    #  logger.debug(dir(event.app.key_processor))
    #  logger.debug(event.app.key_processor.key_buffer)
    #  logger.debug(event.app.key_processor.key_buffer[0].key)
    #  logger.debug(event.app.key_processor.process_keys)
    #  focu = emails[key]
    #  focu.height = 2
    event.app.layout.focus(send_btn)

layout = Layout(body)
application = Application(key_bindings=kb,layout=layout, full_screen=True)

def init_value():
    application.layout.get_buffer_by_name('receivers').text = 'wenxiaoning@gochinatv.com'
    application.layout.get_buffer_by_name('subject').text = '测试主题'
    application.layout.focus(send_btn)

def main():
    init_value()
    application.run()

if __name__ == "__main__":
    main()

