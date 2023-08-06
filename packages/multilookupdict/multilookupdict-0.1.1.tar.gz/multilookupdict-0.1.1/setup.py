# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multilookupdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'multilookupdict',
    'version': '0.1.1',
    'description': 'A dict-like container that allows multiple keys to address the same value.',
    'long_description': '# Multi-Lookup-Dict\n\nA Dict-like container that allows multiple keys to address the same value.\n\n```python\n>>> d = MultiLookupDict()\n>>> d["a_key"] = "some_value"\n>>> d.map_key("a_key", "another_key") # Make "another_key" an alias of "a_key"\n```\nImplemented as two dicts:\n- `MultiLookupDict._data` holds the \'canonical key\' and value\n- `MultiLookupDict._key_to_canonical_map` maps \'alias keys\' onto canonical keys. (Canonical keys are mapped to themselves in this dict)\n\nExternally, all keys (canonical and alias) are treated identically,\nand all refer to the same value, unless a key is reassigned individually with a new value using `__setitem__`\n\n\n\n\nMethods\n-------\n\n`__setitem__`  \n    Sets a key to the value. If a (non-string) iterable is provided\n    as key, each key will be assigned the value.  \n`__getitem__`  \n    [As with standard Python `dict`]  \n`map_key`  \n    Assign the value of one key to another key. Both keys\n    now point to the same value.  \n`keys`  \n    Returns all keys in MultiLookupDict. Returned keys refer to same or different objects.  \n`all_keys`  \n    [Same as `keys`]  \n`values`\n    [Same as `values`]  ',
    'author': 'Richard Hadden',
    'author_email': 'richard.hadden@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richardhadden/multilookupdict',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
