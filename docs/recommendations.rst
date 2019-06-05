.. _recommendations:

Recommendations (Must Read!)
----------------------------

Fixtures That Generate Queries
++++++++++++++++++++++++++++++

If your test case is using fixtures that are generating any database queries, you will end up with unwanted queries being counted in your tests. For that reason, we recommend you to manually request the usage of the ``count_queries`` fixture and put it as the last parameter of your test.

By doing so, you will be sure that the query counter is actually always executed last and does not wrap any other fixtures.

Along side, you might want to still use the plugin's ``count_queries`` marker which is useful to keep your tests separated from the query counting tests.

Your code will look like something like this:

.. code-block:: python

    import pytest


    @pytest.mark.count_queries(autouse=False)
    def test_retrieve_main_menu(fixture_making_queries, count_queries):
        pass


Using ``pytest-django`` Alongside of Counting Queries
+++++++++++++++++++++++++++++++++++++++++++++++++++++

You are most likely using the ``pytest-django`` plugin which is really useful for django testing. By following the previous section's example, you might want to unblock the test database as well. You would do something like this:

.. code-block:: python

    import pytest


    @pytest.mark.django_db
    @pytest.mark.count_queries(autouse=False)
    def test_retrieve_main_menu(any_fixture, other_fixture, count_queries):
        pass
