Customizing the Outputs
=======================

Customizing the console output
++++++++++++++++++++++++++++++

To be done, feel free to open a PR!


Customizing the HTML output
+++++++++++++++++++++++++++

We are using `jinja2 <http://jinja.pocoo.org/>`_ as a template engine for rendering results. You can customize it by passing the ``--template <YOUR_TEMPLATE_PATH>`` option.

The test data are passed to the ``data`` variable. It contains an iterator of:

.. code-block:: python

    [
        ("the module name", [
            "the test name", {"query-count": int},
            ...
        ],
        ...
    ]

.. note::

    We also provide a ``humanize`` function that takes a string a removes from it the ``test_`` prefix.

For example, you would do the following to show all the results:

.. code-block:: jinja

        {% for module_name, module_data in data %}
            <section>
                <h2 class="text-capitalize">{{ humanize(module_name) }}</h2>

                <table class="table table-bordered mb-5">
                    <thead>
                        <tr>
                            <th>Benchmark name</th>
                            <th>Query count</th>
                        </tr>
                    </thead>

                    <tbody>
                        {% for test_entry in module_data %}
                            <tr>
                                <td class="text-capitalize">
                                    <code>{{ humanize(test_entry.test_name) }}</code>
                                </td>
                                <td>
                                    <strong>{{ test_entry['query-count'] }}</strong>
                                </td>
                            </tr>
                        {% else %}
                            <tr>
                                <td colspan="2">
                                    <p>No data.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>
        {% else %}
            <p>No data.</p>
        {% endfor %}
