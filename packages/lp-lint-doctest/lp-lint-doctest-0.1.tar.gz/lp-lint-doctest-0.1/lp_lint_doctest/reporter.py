# Copyright (C) 2013-2013 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the MIT license (see the file LICENSE).
"""Reporting and output helpers."""

__all__ = [
    'Reporter',
]

import logging
import os
import sys


class ConsoleHandler(logging.StreamHandler):
    """A handler that logs to console."""

    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.stream = None  # Not used.

    def emit(self, record):
        self.__emit(record, sys.stdout)

    def __emit(self, record, stream):
        self.stream = stream
        logging.StreamHandler.emit(self, record)

    def flush(self):
        is_flushable = self.stream and hasattr(self.stream, 'flush')
        if is_flushable and not self.stream.closed:
            logging.StreamHandler.flush(self)


logger = logging.getLogger()
logger.propagate = False
logger.addHandler(ConsoleHandler())


class Reporter(object):
    """Common rules for checkers."""
    CONSOLE = object()
    COLLECTOR = object()

    def __init__(self, report_type):
        self.report_type = report_type
        self.piter = None
        self._last_file_name = None
        self.call_count = 0
        self.messages = []

    def __call__(self, line_no, message, base_dir=None, file_name=None):
        """Report a message."""
        self.call_count += 1
        args = (line_no, message, base_dir, file_name)
        if self.report_type == self.COLLECTOR:
            self._message_collector(*args)
        else:
            self._message_console(*args)

    def _message_console(self, line_no, message,
                         base_dir=None, file_name=None):
        """Print the messages to the console."""
        self._message_console_group(base_dir, file_name)
        logger.error('    %4s: %s' % (line_no, message))

    def _message_console_group(self, base_dir, file_name):
        """Print the file name is it has not been seen yet."""
        source = (base_dir, file_name)
        if file_name is not None and source != self._last_file_name:
            self._last_file_name = source
            logger.error('%s' % os.path.join('./', base_dir, file_name))

    def _message_collector(self, line_no, message,
                           base_dir=None, file_name=None):
        self._last_file_name = (base_dir, file_name)
        self.messages.append((line_no, message))
