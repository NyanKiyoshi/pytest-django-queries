from pytest_django_queries.utils import assert_type, raise_error


class Entry(object):
    BASE_FIELDS = [("test_name", "Test Name")]
    REQUIRED_FIELDS = [("query-count", "Queries")]
    OPTIONAL_FIELDS = [("duplicates", "Duplicated")]
    FIELDS = BASE_FIELDS + REQUIRED_FIELDS + OPTIONAL_FIELDS

    def __init__(self, test_name, module_name, data):
        """
        :param data: The test entry's data.
        :type data: dict
        """

        assert_type(data, dict)

        self._raw_data = data
        self.test_name = test_name
        self.module_name = module_name

        for field, _ in self.REQUIRED_FIELDS:
            setattr(self, field, self._get_required_key(field))

        for field, _ in self.OPTIONAL_FIELDS:
            setattr(self, field, self._get_key(field, "UNK"))

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def query_count(self):
        return self["query-count"]

    @property
    def duplicate_count(self):
        return self["duplicates"]

    def _get_key(self, key, default):
        return self._raw_data.get(key, default)

    def _get_required_key(self, key):
        if key in self._raw_data:
            return self._raw_data.get(key)
        raise_error("Got invalid data. It is missing a required key: %s" % key)


def iter_entries(entries):
    for module_name, module_data in sorted(entries.items()):
        assert_type(module_data, dict)

        yield module_name, (
            Entry(test_name, module_name, test_data)
            for test_name, test_data in sorted(module_data.items())
        )


def flatten_entries(file_content):
    entries = []
    for _, data in iter_entries(file_content):
        entries += list(data)
    return entries
