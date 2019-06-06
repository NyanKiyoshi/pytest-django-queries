v1.0.0rc3 - June 6th 2019
+++++++++++++++++++++++++

- Added support for running tests into multiple workers (``pytest-xdist``).


v1.0.0rc2 - June 5th 2019
+++++++++++++++++++++++++

- Renamed the marker description to be more meaningful about was it does.
- Fixed a typo in the project description (PyPi and GitHub).
- Added help texts for named parameters in the cli.
- Fixed the wrong help text saying it is taking an integer when it actually expects a file path.
- Users can now mark tests without having the ``count_queries`` fixture injected automatically if a custom order or manual usage is needed.
- Added a better filtering of unwanted keywords in humanization of test names. It now handles test cases names inside modules (dotted import names).
- Added a ``backup`` command to ``django-queries`` to make it easier of making a copy of the current results.


v1.0.0rc1 - May 24th 2019
+++++++++++++++++++++++++

- Users can now backup/copy their previous results using the ``--django-backup-queries`` parameter when running ``pytest``.
- The HTML cli command now exports to ``django-queries-results.html`` by default instead of ``stdout``, instead, users have to run ``django-queries html -`` for the output to go in ``stdout``.
- The code now enforces the Black code style and Flake 8 checks in addition to isort.


v1.0.0b1 - May 24th 2019
++++++++++++++++++++++++

- Implement a ``diff`` command for comparing results.


v1.0.0a2 - May 17th 2019
++++++++++++++++++++++++

- The requirements that could generate any diverging results between installation have now been freeze.
- A "Read The Docs" documentation has been made and published.
- Guides on how to release and contribute have been added.
- The HTML template has been moved to its own file under the package directory as ``templates/default_bootstrap.jinja2``.
- The Cli commands are now taking optionally the report path file, so it can now be omitted.


v1.0.0a1 - May 13th 2019
++++++++++++++++++++++++

- In #12, stopped storing the benchmark results in a file named after the current date and time.
  Instead, it will always save into ``.django-queries`` and won't contain a ``json`` file extension
  anymore to make it less appealing as it's not meant to be read by a human.
- In #12, dropped the environment variable ``PYTEST_QUERIES_SAVE_PATH`` and replaced
  and introduced the ``--django-db-bench PATH`` option instead, which does exactly the same thing.


v1.0.0.dev1 - May 12th 2019
+++++++++++++++++++++++++++

- Introduced the cli (#3) with two commands:

  - ``show`` that process a given benchmark result to render a summary table
  - ``html`` render the table in HTML, the template can be customized using ``--template <path>``


v0.1.0 - May 7th 2019
+++++++++++++++++++++

- The plugin is now able to support multiple pytest sessions without conflicting (#1)
- The plugin non-longer benchmarks everything but instead, the user is charged to manually flag each test as to be or not to be benchmarked (#1).


v0.0.0 - May 5th 2019
+++++++++++++++++++++

- Initial demo release.
