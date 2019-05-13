## v1.0.0a1 - May 13th 2019
- [x] In #12, stopped storing the benchmark results in a file named after the current date and time.
      Instead, it will always save into `.django-queries` and won't contain a `json` file extension
      anymore to make it less appealing as it's not meant to be read by a human.
- [x] In #12, dropped the environment variable `PYTEST_QUERIES_SAVE_PATH` and replaced
      and introduced the `--django-db-bench PATH` option instead, which does exactly the same thing.

## v1.0.0.dev1 - May 12th 2019
- [x] Introduced the cli (#3) with two commands:
  - [x] `show` that process a given benchmark result to render a summary table
  - [x] `html` render the table in HTML, the template can be customized using `--template <path>`

## v0.1.0 - May 7th 2019
- [x] The plugin is now able to support multiple pytest sessions without conflicting (#1)
- [x] The plugin non-longer benchmarks everything but instead, the user is charged to manually flag each test as to be or not to be benchmarked (#1).

## v0.0.0 - May 5th 2019
- [x] Initial demo release.
