````# Contributing

[Local Development]: #local-development

## Local Development

1. Install the [`uv`] package manager
2. Clone the project locally
3. Run:

   ```shell
   uv sync --all-extras --all-groups --inexact
   ```

   Or run (Unix-based systems only):

   ```shell
   make install
   ```

[`uv`]: https://docs.astral.sh/uv/

## Submitting Changes (Pull Requests)

1. Update the [changelog]
2. Make sure to run the `pre-commit` command to lint and format the code
   (automatically installed in the [Local Development] step)
3. We use Codecov (code coverage service) to report the test coverage of your changes.
   We have a strict 100% coverage, meaning that all the code is covered by tests.
   Please test all your changes and test them hastily, don’t test just for the sake
   of testing and to get a proper coverage. We want the tests to prevent any error and
   any potential breaking from changes!
4. Finally, make sure you are using the latest version of the dependencies and that
   you have read our documentations.
5. If you need to test the documentation, you can run the following commands:

   ```shell
   $ cd docs/
   $ make build
   ```

   Then, open `_build/index.html` in your browser.

[changelog]: ./CHANGELOG.rst
````