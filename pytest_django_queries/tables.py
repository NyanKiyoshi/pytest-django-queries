from os import getenv

import click
from beautifultable import BeautifulTable
from jinja2 import Template

from pytest_django_queries.utils import assert_type, raise_error

HTML_TEMPLATE = '''
<!doctype HTML>
<html lang="en_US">
    <head>
        <title>Results</title>
        <link rel="stylesheet" 
              href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" 
              integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
              crossorigin="anonymous" />
        <style>
            tbody tr > td:last-child {
                width: 10rem
            }
        </style>
    </head>
    
    <body class="container-fluid">
        <h1 class="text-center mt-5 mb-5">Benchmark Results</h1>
        
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
    </body>
</html>
'''
TABLE_ATTRIBUTES = 'id="info-table" class="table table-bordered"'


def format_underscore_name_to_human(name):
    if name.startswith('test'):
        _, name = name.split('test', 1)
    return name.replace('_', ' ')


class TestEntryData(object):
    BASE_FIELDS = [
        ('test_name', 'Test Name')
    ]
    REQUIRED_FIELDS = [
        ('query-count', 'Queries'),
    ]
    FIELDS = BASE_FIELDS + REQUIRED_FIELDS

    def __init__(self, test_name, data):
        """
        :param data: The test entry's data.
        :type data: dict
        """

        assert_type(data, dict)

        self._raw_data = data
        self.test_name = test_name

        for field, _ in self.REQUIRED_FIELDS:
            setattr(self, field, self._get_required_key(field))

    def _get_required_key(self, key):
        if key in self._raw_data:
            return self._raw_data.get(key)
        raise_error('Got invalid data. It is missing a required key: %s' % key)


def iter_entries(entries):
    for module_name, module_data in sorted(entries.items()):
        assert_type(module_data, dict)

        yield module_name, (
            TestEntryData(test_name, test_data)
            for test_name, test_data in sorted(module_data.items()))


def print_entries(data):
    table = BeautifulTable()
    table.column_headers = ['Module', 'Tests']
    for module_name, module_entries in iter_entries(data):
        subtable = BeautifulTable()
        subtable.column_headers = [field for _, field in TestEntryData.FIELDS]
        for entry in module_entries:
            subtable.append_row([
                getattr(entry, field) for field, _ in TestEntryData.FIELDS])
        table.append_row([module_name, subtable])
    click.echo(table)


def print_entries_as_html(data, template):
    template = template or Template(HTML_TEMPLATE)
    html_content = template.render(
        data=iter_entries(data), humanize=format_underscore_name_to_human)
    click.echo(html_content, nl=False)
