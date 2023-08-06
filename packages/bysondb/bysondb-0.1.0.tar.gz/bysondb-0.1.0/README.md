# BysonDB

A serverless keyvalue and document based database using BSON.

## What the heck is BSON?

BSON is short for **Binary JavaScript Object Notation**. It is the binary encoding of JSON, created by MongoDB, and is used in their database. It allows for more datatypes, such as dates and bytes, that JSON does not allow. You can read more about it's purpose, and it's similarites and differences to JSON [here](https://bsonspec.org/).

---

# Usage:

## Installation:
```bash
pip install bysondb
```

## Key -> Value database:
A database just like normal JSON, with each key coresponding to a value 
```py
import datetime
from bysondb import BysonDB

# Create a database with a path to a file. The suffix
# will be changed to .bson, even if there is no suffix
my_db = BysonDB('path/to/database/file.bson')

# Set values like a normal dictionary
my_db["name"] = "John"
my_db["age"] = 30

# Get values in the same way
print(f"My name is {my_db['name']}. I am {my_db['age']} years old.")

# Some objects like datetimes can be used as well
# Not all objects can be serialized
my_db["date"] = datetime.datetime.now()

print(f"Today's date is {my_db['date'].strftime('%x')}")

# Deleteing a key. Can't be undone, so be careful.
my_db.remove("test")
```

## Document based database
A database structure similar to MongoDB, with a single collection of objects
```py
from bysondb import BysonDocumentDB

# Creating a database is the same with the BysonDB,
# but using BysonDocumentDB
my_db = BysonDocumentDB('path/to/database/file.bson')

# Insert a single object to the database
person = {
    "name": "John",
    "age": 30
}
my_db.insert_one(person)

# Insert multiuple objects into the database
people = [
    {"name": "Joe"},
    {"name": "Steve"},
    {"key": "value"}
]
my_db.insert_many(people)


# Get objects as dicts from the database using a query

# Get all objects
all_objects = my_db.find({})

# Get an object where the key 'debug' is True
debug_objects = my_db.find({"debug": True})

# Find a maximum of 5 objects where the key 'key' is 'value'
objects = my_db.find({"key": "value"}, limit=5)

# Removing values is like finding them, with a search query and a limit
my_db.remove({"remove": True})
my_db.remove({"random_number": 5}, limit=1})
```

---

This package uses [bson](https://github.com/py-bson/bson), a package for the BSON codec that does not rely on MongoDB.

This package was formatted using [black](https://black.rtfd.io).