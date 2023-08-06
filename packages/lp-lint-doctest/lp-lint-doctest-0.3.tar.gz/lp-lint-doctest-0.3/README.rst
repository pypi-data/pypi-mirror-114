`lp-lint-doctest <https://git.launchpad.net/lp-lint-doctest>`_ is a style
checker for `Python doctests
<https://docs.python.org/3/library/doctest.html>`_ stored in text files (as
opposed to doctests stored in docstrings), optimized for use in `Launchpad
development <https://dev.launchpad.net/>`_.  It applies the following
checks:

 * Comments should be in the narrative part of the doctest (i.e. in
   unindented text) rather than in Python examples.
 * Narrative text lines are limited to 78 characters.
 * Source lines in examples (beginning with ``>>>`` or ``...``) are limited
   to 70 characters.
 * Expected output lines in examples are limited to 74 characters.
 * Source and expected output lines should be indented by exactly four
   spaces.
 * There should be no trailing whitespace.
 * reStructuredText-style headings should be used, not MoinMoin-style.

A ``# noqa`` comment in any source line in an example suppresses the
comment, line length, indentation, and trailing whitespace checks for all
lines in that example.

In addition, ``lp-lint-doctest`` runs `pyflakes
<https://pypi.org/project/pyflakes/>`_ on the accumulated source code of
each doctest file.

This project was split out from Curtis Hovey's `pocket-lint
<https://launchpad.net/pocket-lint>`_ project.  Since that was written, many
other excellent linters have arisen for most of the other source types
supported by ``pocket-lint``, but there seems to be no other viable
replacement for its doctest checks.

``lp-lint-doctest`` supports `pre-commit <https://pre-commit.com/>`_.  To
use it, add the following to the ``repos`` section of your
``.pre-commit-config.yaml`` file::

    -   repo: https://git.launchpad.net/lp-lint-doctest
        rev: ''  # pick a git tag to point to
        hooks:
        -   id: lp-lint-doctest

If you need to add a custom doctest option flag, then add ``args:
[--allow-option-flag, MY_CUSTOM_FLAG_NAME]``.
