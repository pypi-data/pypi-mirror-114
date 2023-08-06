# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bysondb']

package_data = \
{'': ['*']}

install_requires = \
['bson>=0.5.10,<0.6.0']

setup_kwargs = {
    'name': 'bysondb',
    'version': '0.1.0',
    'description': 'A simple BSON database written in Python',
    'long_description': '# BysonDB\n\nA serverless keyvalue and document based database using BSON.\n\n## What the heck is BSON?\n\nBSON is short for **Binary JavaScript Object Notation**. It is the binary encoding of JSON, created by MongoDB, and is used in their database. It allows for more datatypes, such as dates and bytes, that JSON does not allow. You can read more about it\'s purpose, and it\'s similarites and differences to JSON [here](https://bsonspec.org/).\n\n---\n\n# Usage:\n\n## Installation:\n```bash\npip install bysondb\n```\n\n## Key -> Value database:\nA database just like normal JSON, with each key coresponding to a value \n```py\nimport datetime\nfrom bysondb import BysonDB\n\n# Create a database with a path to a file. The suffix\n# will be changed to .bson, even if there is no suffix\nmy_db = BysonDB(\'path/to/database/file.bson\')\n\n# Set values like a normal dictionary\nmy_db["name"] = "John"\nmy_db["age"] = 30\n\n# Get values in the same way\nprint(f"My name is {my_db[\'name\']}. I am {my_db[\'age\']} years old.")\n\n# Some objects like datetimes can be used as well\n# Not all objects can be serialized\nmy_db["date"] = datetime.datetime.now()\n\nprint(f"Today\'s date is {my_db[\'date\'].strftime(\'%x\')}")\n\n# Deleteing a key. Can\'t be undone, so be careful.\nmy_db.remove("test")\n```\n\n## Document based database\nA database structure similar to MongoDB, with a single collection of objects\n```py\nfrom bysondb import BysonDocumentDB\n\n# Creating a database is the same with the BysonDB,\n# but using BysonDocumentDB\nmy_db = BysonDocumentDB(\'path/to/database/file.bson\')\n\n# Insert a single object to the database\nperson = {\n    "name": "John",\n    "age": 30\n}\nmy_db.insert_one(person)\n\n# Insert multiuple objects into the database\npeople = [\n    {"name": "Joe"},\n    {"name": "Steve"},\n    {"key": "value"}\n]\nmy_db.insert_many(people)\n\n\n# Get objects as dicts from the database using a query\n\n# Get all objects\nall_objects = my_db.find({})\n\n# Get an object where the key \'debug\' is True\ndebug_objects = my_db.find({"debug": True})\n\n# Find a maximum of 5 objects where the key \'key\' is \'value\'\nobjects = my_db.find({"key": "value"}, limit=5)\n\n# Removing values is like finding them, with a search query and a limit\nmy_db.remove({"remove": True})\nmy_db.remove({"random_number": 5}, limit=1})\n```\n\n---\n\nThis package uses [bson](https://github.com/py-bson/bson), a package for the BSON codec that does not rely on MongoDB.\n\nThis package was formatted using [black](https://black.rtfd.io).',
    'author': 'Patrick Brennan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AM2i9/bysondb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
