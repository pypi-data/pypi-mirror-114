# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongo_the_sql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymongo-the-sql',
    'version': '0.0.2',
    'description': 'A sql wrapper made to mimic the pymongo syntax in order to simplify sql syntax.',
    'long_description': '# pymongo-the-sql\nA sql wrapper made to mimic the pymongo syntax in order to simplify sql syntax.\n\n## Docs\n\n### Usage\n\n    from pymongo_the_sql.pymongo_the_sql import PyMongoTheSql\n    PyMongoTheSql("../tests/test.sqlite3")\n    <pymongo_the_sql.pymongo_the_sql.PyMongoTheSql object at 0x7f60878e8e80>\n    client = PyMongoTheSql("../tests/test.sqlite3")\n    client = PyMongoTheSql("../tests")\n    db = client.get_database("test")\n    db["users"]\n    <pymongo_the_sql.pymongo_the_sql.PyMongoTheSql object at 0x7f6087763400>\n    users = db["users"]\n    users.find({"id": "1"})\n\n### Api\n\n#### Update\n\nUpdates values for all specified columns where the conditions are True.\n    update(columns_values: dict, conditions: dict[Optional], operator: str[Optional]) -> bool\n\nUpdates values for all specified columns where the conditions are True. Use the values tuple to update Blob type objects.\n    update_blob(columns_values: dict, values: tuple[Optional], conditions: dict[Optional], operator: str[Optional])\n\nUpdates values for all specifed columns on the first row where the conditions are True.\n    update_one(columns_values: dict, conditions: dict[Optional])\n\nUpdates values for all specified columns on every row.\n    update_all(columns_values: dict[Optional]) -> bool\n\n#### Find\n\nReturns the specified columns on all rows the conditions are True.\n    find(conditions: dict, columns: dict, operator: str) -> dict\n\nReturns the specified columns on the first row the conditions are True.\n    find_one(conditions: dict, columns: list, operator: str) -> dict\n\nReturns the whole table.\n    find_all() -> dict\n\nReturns the specified columns on the last row the conditions are True.\n    find_last(conditions: dict[Optional], columns: list[Optional], operator: str[Optional]) -> dict\n\nReturns how many rows in the table.\n    find_all_and_count() -> int\n\nReturns how many rows the conditions are True.\n    find_and_count(conditions: dict[Optional], columns: list[Optional], operator: str[Optional]) -> int\n\n#### Insert\n\nInserts the values in the specified columns.\n    insert(columns_values: dict) -> bool',
    'author': 'Marcus Bader',
    'author_email': 'marcus@appsight.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://appsight.se',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
