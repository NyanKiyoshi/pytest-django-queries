# Example Application for `pytest-django-queries`

This is a simple dummy application to showcase how the `pytest-django-queries`
plugin works.

> [!NOTE]
> This project is voluntarily unoptimized, views should run only 1 SQL query
> but instead they are running N of them.

## Usage

1. The [`uv`] package manager is needed
2. Clone the project locally
3. Install dependencies:
   ```shell
   uv sync --all-extras  --all-groups --inexact
   ```

   Or run (Unix-based systems only):

   ```shell
   make install
   ```
4. Run pytest:

   ```shell
   pytest ./
   ```
5. Show queries:

   ```shell
   $ django-queries
   +------------+---------------------------------------------+
   |   Module   |                    Tests                    |
   +------------+---------------------------------------------+
   | test_views | +------------------+---------+------------+ |
   |            | |    Test Name     | Queries | Duplicated | |
   |            | +------------------+---------+------------+ |
   |            | | test_book_detail |    3    |     1      | |
   |            | +------------------+---------+------------+ |
   |            | | test_index_page  |   11    |     0      | |
   |            | +------------------+---------+------------+ |
   +------------+---------------------------------------------+
   ```

[`uv`]: https://docs.astral.sh/uv/
