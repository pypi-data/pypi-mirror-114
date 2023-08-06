========================
NEWS for lp-lint-doctest
========================

0.3 (2021-07-27)
================

  - Allow ``# noqa`` comments to suppress comment checks as well.

0.2 (2021-07-25)
================

  - Add ``--allow-option-flag`` command-line option to register custom
    ``doctest`` option flags.
  - Allow comments in source lines in examples if they contain ``doctest``
    directives.
  - Allow suppressing checks for an example by adding a ``# noqa`` comment
    to any of its source lines.

0.1 (2021-07-24)
================

  - Initial release, split out from pocket-lint.
