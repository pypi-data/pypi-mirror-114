# Copyright (C) 2009-2013 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the MIT license (see the file LICENSE).

"""Reformat a doctest to Launchpad style."""

__all__ = [
    'DoctestReviewer',
]

from argparse import ArgumentParser
import ast
from doctest import (
    DocTestParser,
    Example,
    register_optionflag,
    )
import os
import re
import sys

from pyflakes.checker import Checker as PyFlakesChecker

from lp_lint_doctest.reporter import Reporter


class DoctestReviewer(object):
    """Check doctests."""
    rule_pattern = re.compile(r'([=~-])+[ ]*$')
    moin_pattern = re.compile(r'^(=+)[ ](.+)[ ](=+[ ]*)$')

    SOURCE = 'source'
    WANT = 'want'
    NARRATIVE = 'narrative'

    def __init__(self, file_path, doctest, reporter=None, options=None):
        self.doctest = doctest
        self.file_path = file_path
        self.base_dir = os.path.dirname(file_path)
        self.file_name = os.path.basename(file_path)
        self.code_lines = []
        self.last_bad_indent = 0
        self.has_printed_filename = False
        self._reporter = reporter or Reporter(Reporter.CONSOLE)
        self.options = options

    def get_parts(self):
        parser = DocTestParser()
        try:
            return parser.parse(self.doctest, self.file_path)
        except ValueError as error:
            # Output code without unicode literals needs to be normalised
            # largely for the test suite, and somewhat for the person reading
            # message.
            message = str(error).replace("u'", "'")
            self._print_message(message, 0)
            return []

    def _print_message(self, message, lineno):
        """Print the error message with the lineno.

        :param message: The message to print.
        :param lineno: The line number the message pertains to.
        """
        self._reporter(
            int(lineno), message,
            base_dir=self.base_dir, file_name=self.file_name)

    def _is_formatted(self, text):
        """Return True if the text is pre-formatted, otherwise False.

        :param: text a string, or a list of strings.
        """
        if isinstance(text, list):
            text = text[0]
        return text.startswith(' ')

    def _walk_part(self, part):
        """Walk a single doctest part: yield the line and kind.

        Yield the content of the line, and its kind (SOURCE, WANT, NARRATIVE).
        SOURCE and WANT lines are stripped of indentation, SOURCE is also
        stripped of the interpreter symbols.

        :param part: One of the items returned by DocTestParser.parse.
        """
        if isinstance(part, Example):
            for line in part.source.splitlines():
                kind = DoctestReviewer.SOURCE
                yield line, kind
            for line in part.want.splitlines():
                kind = DoctestReviewer.WANT
                yield line, kind
        else:
            kind = DoctestReviewer.NARRATIVE
            for line in part.splitlines():
                yield line, kind

    def _apply(self, line_methods):
        """Call each line_method for each line in the doctest.

        :param line_methods: a list of methods that accept lineno, part,
            line, and kind as arguments. Each method must return the line
            for the next method to process.
        """
        lineno = 0
        for part in self.get_parts():
            if part == '':
                continue
            block_start = lineno + 1
            if isinstance(part, Example):
                skip_check = bool(re.search(r"# noqa", part.source, re.I))
            else:
                skip_check = False
            block = []
            for line, kind in self._walk_part(part):
                lineno += 1
                self._append_source(kind, line)
                block.append((line, kind))
            if not skip_check:
                self._check_block(block_start, part, block, line_methods)

    def _append_source(self, kind, line):
        """Update the list of source code lines seen."""
        if kind == self.SOURCE:
            self.code_lines.append(line)
        else:
            self.code_lines.append('')

    def _check_block(self, block_start, part, block, line_methods):
        """Check all lines in the current block.

        :param block_start: The number of the first line in the block.
        :param part: One of the items returned by DocTestParser.parse.
        :param block: A parsed iterable of (line, kind).
        :param line_methods: a list of methods that accept lineno, line,
            and kind as arguments. Each method must return the line for
            the next method to process.
        """
        for i, (line, kind) in enumerate(block):
            for method in line_methods:
                line = method(block_start + i, part, line, kind)
                if line is None:
                    break

    def check(self):
        """Check the doctest for style and code issues.

        1. Check line lengths.
        2. Check that headings are not in Moin format.
        3. Check indentation.
        4. Check trailing whitespace.
        """
        self.code_lines = []
        self.last_bad_indent = 0
        self.has_printed_filename = False
        self.check_source_comments()
        line_checkers = [
            self.check_length,
            self.check_heading,
            self.check_indentation,
            self.check_trailing_whitespace,
        ]
        self._apply(line_checkers)
        code = '\n'.join(self.code_lines)
        self.check_source_code(code)

    def check_source_comments(self):
        """Comments are not appropriate in source examples."""
        # DocTestParser.parse removes source lines that consist only of
        # comments, so we have to parse the file to some extent ourselves.
        first_source_re = re.compile(r"^ *>>>")
        subsequent_source_re = re.compile(r"^ *\.\.\.")
        check_re = re.compile(r"^ *(?:>>>|\.\.\.) #(?! *(?:doctest:|noqa))")
        kind = DoctestReviewer.NARRATIVE
        block = []
        skip_check = False

        def check():
            if kind == DoctestReviewer.NARRATIVE or skip_check:
                return
            for lineno, line in block:
                if check_re.match(line):
                    self._print_message(
                        'Comment belongs in narrative.', lineno + 1)

        for lineno, line in enumerate(self.doctest.splitlines()):
            if kind == DoctestReviewer.NARRATIVE:
                if first_source_re.match(line):
                    # We don't need to check narrative blocks here.
                    block = []
                    kind = DoctestReviewer.SOURCE
            elif kind == DoctestReviewer.SOURCE:
                if first_source_re.match(line):
                    check()
                    block = []
                    skip_check = False
                elif subsequent_source_re.match(line):
                    pass
                elif line.strip():
                    check()
                    block = []
                    kind = DoctestReviewer.WANT
                else:
                    # Invalid, but we aren't worried about that here.
                    check()
                    block = []
                    kind = DoctestReviewer.NARRATIVE
            elif kind == DoctestReviewer.WANT:
                if first_source_re.match(line):
                    check()
                    block = []
                    kind = DoctestReviewer.SOURCE
                elif not line.strip():
                    check()
                    block = []
                    kind = DoctestReviewer.NARRATIVE

            block.append((lineno, line))

            if (kind == DoctestReviewer.SOURCE and
                    re.search(r'# noqa', line, re.I)):
                skip_check = True

        check()

    def is_code_comment(self, line):
        """Return True if the line is a code comment."""
        comment_pattern = re.compile(r'^\s+#')
        return comment_pattern.match(line) is not None

    def check_length(self, lineno, part, line, kind):
        """Check the length of the line.

        Each kind of line has a maximum length:

        * NARRATIVE: 78 characters.
        * SOURCE: 70 characters (discounting indentation and interpreter).
        * WANT: 74 characters (discounting indentation).
        """
        if kind == DoctestReviewer.NARRATIVE and self.is_code_comment(line):
            # comments follow WANT rules because they are in code.
            kind = DoctestReviewer.WANT
            line = line.lstrip()
        length = len(line)
        if kind == DoctestReviewer.NARRATIVE and length > 78:
            self._print_message('%s exceeds 78 characters.' % kind, lineno)
        elif kind == DoctestReviewer.WANT and length > 74:
            self._print_message('%s exceeds 78 characters.' % kind, lineno)
        elif kind == DoctestReviewer.SOURCE and length > 70:
            self._print_message('%s exceeds 78 characters.' % kind, lineno)
        else:
            # This line has a good length.
            pass
        return line

    def check_indentation(self, lineno, part, line, kind):
        """Check the indentation of the SOURCE or WANT line."""
        if kind == DoctestReviewer.NARRATIVE or not isinstance(part, Example):
            return line
        if part.indent != 4:
            if self.last_bad_indent != lineno - 1:
                self._print_message('%s has bad indentation.' % kind, lineno)
            self.last_bad_indent = lineno
        return line

    def check_trailing_whitespace(self, lineno, part, line, kind):
        """Check for the presence of trailing whitespace in the line."""
        if line.endswith(' '):
            self._print_message('%s has trailing whitespace.' % kind, lineno)
        return line

    def check_heading(self, lineno, part, line, kind):
        """Check for narrative lines that use moin headers instead of RST."""
        if kind != DoctestReviewer.NARRATIVE:
            return line
        moin = self.moin_pattern.match(line)
        if moin is not None:
            self._print_message('%s uses a moin header.' % kind, lineno)
        return line

    def check_source_code(self, code):
        """Check for source code problems in the doctest using pyflakes.

        The most common problem found are unused imports. `UndefinedName`
        errors are suppressed because the test setup is not known.
        """
        if code == '':
            return
        try:
            tree = compile(code, self.file_path, "exec", ast.PyCF_ONLY_AST)
        except (SyntaxError, IndentationError) as exc:
            lineno = exc.lineno or 0
            line = exc.text or ''
            if line.endswith("\n"):
                line = line[:-1]
            self._print_message(
                'Could not compile:\n    %s' % line, lineno)
        else:
            warnings = PyFlakesChecker(tree)
            for warning in warnings.messages:
                if 'undefined name ' in str(warning):
                    continue
                dummy, lineno, message = str(warning).split(':')
                self._print_message(message.strip(), lineno)


def main(argv=None):
    """Run the operations requested from the command line."""
    if argv is None:
        argv = sys.argv
    parser = ArgumentParser()
    parser.add_argument(
        "--allow-option-flag", dest="allow_option_flags",
        action="append", default=[],
        help="Allow this custom doctest option flag.")
    parser.add_argument("paths", nargs="+", help="Paths to check.")
    args = parser.parse_args(argv[1:])

    for name in args.allow_option_flags:
        register_optionflag(name)

    reporter = Reporter(Reporter.CONSOLE)
    for file_path in args.paths:
        with open(file_path) as doctest_file:
            doctest_data = doctest_file.read()
        reviewer = DoctestReviewer(file_path, doctest_data, reporter=reporter)
        reviewer.check()
    return 1 if reporter.call_count else 0
