# Copyright (C) 2012-2013 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the MIT license (see the file COPYING).

from lp_lint_doctest.tests import CheckerTestCase


class ReporterTestCase(CheckerTestCase):

    def test_init(self):
        self.assertEqual(self.reporter.COLLECTOR, self.reporter.report_type)

    def test_call(self):
        self.reporter(12, "test", base_dir='./lib', file_name='eg.py')
        self.assertEqual(1, self.reporter.call_count)
        self.assertEqual(('./lib', 'eg.py'), self.reporter._last_file_name)
        self.assertEqual([(12, 'test')], self.reporter.messages)
