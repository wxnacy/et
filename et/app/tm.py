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
        '/tmp/tm.log', maxBytes=104857600, backupCount=20
    )
    #  error_file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    return logger

logger = create_logger()

import os

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.sql import SqlLexer

sql_completer = WordCompleter([
    'abort', 'action', 'add', 'after', 'all', 'alter', 'analyze', 'and',
    'as', 'asc', 'attach', 'autoincrement', 'before', 'begin', 'between',
    'by', 'cascade', 'case', 'cast', 'check', 'collate', 'column',
    'commit', 'conflict', 'constraint', 'create', 'cross', 'current_date',
    'current_time', 'current_timestamp', 'database', 'default',
    'deferrable', 'deferred', 'delete', 'desc', 'detach', 'distinct',
    'drop', 'each', 'else', 'end', 'escape', 'except', 'exclusive',
    'exists', 'explain', 'fail', 'for', 'foreign', 'from', 'full', 'glob',
    'group', 'having', 'if', 'ignore', 'immediate', 'in', 'index',
    'indexed', 'initially', 'inner', 'insert', 'instead', 'intersect',
    'into', 'is', 'isnull', 'join', 'key', 'left', 'like', 'limit',
    'match', 'natural', 'no', 'not', 'notnull', 'null', 'of', 'offset',
    'on', 'or', 'order', 'outer', 'plan', 'pragma', 'primary', 'query',
    'raise', 'recursive', 'references', 'regexp', 'reindex', 'release',
    'rename', 'replace', 'restrict', 'right', 'rollback', 'row',
    'savepoint', 'select', 'set', 'table', 'temp', 'temporary', 'then',
    'to', 'transaction', 'trigger', 'union', 'unique', 'update', 'using',
    'vacuum', 'values', 'view', 'virtual', 'when', 'where', 'with',
    'without'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})

#  print(first_keywords)
#  print(sql_completer)

def make_completions(doc):
    logger.debug(dir(doc))
    for k in dir(doc):
        if not k.startswith("_"):
            if k.startswith("get") or k.startswith("find"):
                try:
                    logger.debug(f'{k}: {getattr(doc, k)()}')
                except Exception as e:
                    logger.debug(f'{k}: {getattr(doc, k)}')

            else:
                logger.debug(f'{k}: {getattr(doc, k)}')
    logger.debug(doc.get_word_before_cursor())
    last_word = doc.get_word_before_cursor()
    last_word = last_word.lower()
    first_keywords = ('select show insert delete explain').split()
    first_keywords = list(filter(lambda x: x.startswith(last_word),
        first_keywords))
    first_completer = [Completion(first_keywords[i],
        start_position=-len(last_word)) for i in range(len(first_keywords))]
    return first_completer

class MyCustomCompleter(Completer):
    def get_completions(self, doc, complete_event):
        #  print(doc, dir(doc))
        #  print(doc.text, doc.current_char, doc.current_line, doc.line_count)
        #  yield from first_completer

        #  yield Completion('completion', start_position=-1)
        for c in make_completions(doc):
            yield c

def main():
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer),
        completer=MyCustomCompleter(),
        #  completer=sql_completer,
        style=style,
        auto_suggest=AutoSuggestFromHistory(),
        history=FileHistory(f'{os.getenv("HOME")}/.tm_history')
    )

    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print('You entered:', text)
    print('GoodBye!')

if __name__ == '__main__':
    main()
