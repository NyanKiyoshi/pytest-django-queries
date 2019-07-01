Getting Started
===============

``pytest-django-queries`` is pytest plugin tool for measuring the database query count of a django project. It captures the SQL queries of marked tests to generate reports from them that can then be analyzed, proceeded and even integrated to CIs and GitHub as a peer reviewing tool (bot).

This is used to detect and correct features that are missing optimizations or that should be rethought, and which parts are doing great.

This is also used to quickly see and compare differences of made changes through the included diff tool.

This tool supports the Python versions: 2.7, 3.4, 3.5, 3.6, 3.7, and 3.8.


Quick Start
+++++++++++
1. Install the tool by running ``pip install pytest-django-queries``;
2. Use the plugin by marking tests or by using the provided fixture:

    .. code-block:: python

        import pytest


        @pytest.mark.count_queries
        def test_query_performances():
            Model.objects.all()


        # Or...
        def test_another_query_performances(count_queries):
            Model.objects.all()

3. Run ``pytest``;
4. Then use ``django-queries show`` to show the results directly into your console:

    .. code-block:: text

        +---------+--------------------------------------+
        | Module  |          Tests                       |
        +---------+--------------------------------------+
        | module1 | +-----------+---------+------------+ |
        |         | | Test Name | Queries | Duplicated | |
        |         | +-----------+---------+------------+ |
        |         | |   test1   |    0    |     0      | |
        |         | +-----------+---------+------------+ |
        |         | |   test2   |    1    |     0      | |
        |         | +-----------+---------+------------+ |
        +---------+--------------------------------------+
        | module2 | +-----------+---------+------------+ |
        |         | | Test Name | Queries | Duplicated | |
        |         | +-----------+---------+------------+ |
        |         | |   test1   |   123   |     0      | |
        |         | +-----------+---------+------------+ |
        +---------+--------------------------------------+

5. Or for a nicer presentation, use ``django-queries html`` to export the results as HTML. See `this example <./html_export_results.html>`_ for a demo!

    .. image:: _static/html_export_results.png
        :width: 500 px
        :align: center

6. By running it twice with the option described :ref:`here <diff_usage>` and by running ``django-queries diff`` you will get something like this:

    .. image:: _static/diff_results.png
        :width: 500 px
        :align: center


.. warning::

    Please take a quick look at our :ref:`recommendations <recommendations>` before starting using the plugin in your project tests.


Getting Help
============
Feel free to `open an issue <https://github.com/NyanKiyoshi/pytest-django-queries/issues>`_ in our GitHub repository! Or reach `hello@vanille.bid <mailto:hello@vanille.bid>`_.


More Topics
===========

.. toctree::
    :hidden:

    self

.. toctree::
    :maxdepth: 2

    recommendations
    diff
    customize
    usage
    contributing
    changelog
