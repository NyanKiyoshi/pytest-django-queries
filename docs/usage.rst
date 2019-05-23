CLI Usage
=========

.. code-block:: text

    Usage: django-queries [OPTIONS] COMMAND [ARGS]...

      Command line tool for pytest-django-queries.

    Options:
      --help  Show this message and exit.

    Commands:
      html  Render the results as HTML instead of a raw table.
      show  View a given rapport.


The HTML Command
++++++++++++++++

.. code-block:: text

    Usage: django-queries html [OPTIONS] [INPUT_FILE]

    Render the results as HTML instead of a raw table.

    Options:
        --template INTEGER
        --help              Show this message and exit.


The SHOW Command
++++++++++++++++

.. code-block:: text

    Usage: django-queries show [OPTIONS] [INPUT_FILE]

    View a given rapport.

    Options: none


The DIFF Command
++++++++++++++++

.. code-block:: text

    Usage: django-queries diff [OPTIONS] [LEFT_FILE] [RIGHT_FILE]

    Render the diff as a console table with colors.

    Options: none

:ref:`More details on how to use the diff command properly. <diff_usage>`
