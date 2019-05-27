Contributing
============

To contribute, you can fork us! And open any pull request or tackle any issue in our `GitHub repository <https://github.com/NyanKiyoshi/pytest-django-queries/issues>`_.


Recommendations
+++++++++++++++

- Try to be on one of the latest master versions.
- Try to always put and commit your change sets into a new and meaningful branch in your fork.
- Update the changelog file with the changes you made.


Code Style
++++++++++

We are using `Black <https://github.com/python/black>`_ and `Flake 8 <http://flake8.pycqa.org/en/latest/>`_ to ensure a consistent code-style and reduce common Python issues in changes.

You can install a checker by running ``pre-commit install`` after installing our development requirements (``pip install -e '.[dev]'``). After that, you can add your changes through ``git`` and run ``pre-commit`` to check if your changes are issue-free.


Pull Request Review Process
+++++++++++++++++++++++++++

Your contributions will get reviewed and will receive comments, remarks and suggestion to get the best of your pull request! It may take time, days or even weeks before you get a review from us. But don’t worry, we won’t forget about it, it just mean it is in a backlog because we are too busy for now.

You will get reviews from bots (CIs) that will succeed or fail. Mostly from travis-ci and codecov. Please be careful about them, they are important checks that we get your contribution denied as long as those checks are not passing.

Travis-ci is there to check that your changes work (tests and linters). If travis fails, it means something is wrong with your changes. Look at the logs, it will tell you what’s going on!

Codecov is there to report the test coverage of your changes. We have a strict 100% coverage, meaning that all the code is covered by automatic tests. Please test all your changes and test them hastily, don’t test just for the sake of testing and to get a proper coverage... it’s wrong. We want the tests to prevent any error and any potential breaking from changes!

Finally, make sure you are using the latest version of the dependencies and that you have read our documentations.
