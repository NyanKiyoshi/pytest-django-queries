.. _diff_usage:

The Diff Command
----------------

The plugin can backup the test results for you if you run the ``django-queries backup [BACKUP_PATH]`` command. It will create a backup to ``.pytest-query.old`` by default if previous results were found.

.. warning::

    Bear in mind that it will override any existing backup file in the provided or default path.

After running ``pytest`` again, you can run ``django-queries diff`` to show the changes. Make sure you actually had previous results, otherwise it will have nothing to compare.
