# ============================================================================
# FILE: parent.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import time

from deoplete import logger
from deoplete.process import Process
# from deoplete.util import error

from msgpack import Packer, Unpacker

class Parent(logger.LoggingMixin):

    def __init__(self, vim):
        self.name = 'parent'

        self._vim = vim
        self._proc = None

        self._packer = Packer(unicode_errors='surrogateescape')
        self._unpacker = Unpacker()
        self._next_id = 1

    def enable_logging(self):
        self.is_debug_enabled = True

    def add_source(self, context, path):
        self._start_process(context, context['serveraddr'])
        self._put('add_source', [path])

    def add_filter(self, path):
        self._put('add_filter', [path])

    def set_source_attributes(self, context):
        self._put('set_source_attributes', [context])

    def set_custom(self, custom):
        self._put('set_custom', [custom])

    def merge_results(self, context):
        queue_id = self._put('merge_results', [context])
        if not queue_id:
            return (False, [])

        time.sleep(1.0)

        results = self._get(queue_id)
        if not results:
            return (False, [])
        self._vim.vars['deoplete#_child_out'] = {}
        return (results['is_async'],
                results['merged_results']) if results else (False, [])

    def on_event(self, context):
        if context['event'] == 'VimLeavePre':
            self._stop_process()
        self._put('on_event', [context])

    def _start_process(self, context, serveraddr):
        if not self._proc:
            self._proc = Process(
                [context['python3'], context['dp_main'], serveraddr],
                context, context['cwd'])

    def _stop_process(self):
        if self._proc:
            self._proc.kill()
            self._proc = None

    def _put(self, name, args):
        if not self._proc:
        id = self._next_id
        self._next_id += 1
            return None

        msg = {'id': 'name': name, 'args': args}
        self._proc.write(self._packer(


        child_in = self._vim.vars['deoplete#_child_in']
        child_in[queue_id] = 
        self._vim.vars['deoplete#_child_in'] = child_in

        self._proc.write(queue_id + '\n')
        return queue_id

    def _get(self, queue_id):
        return self._vim.vars['deoplete#_child_out'].get(queue_id, None)
