from bysondb.errors import InvalidTypeException
from typing import Optional, Union, Iterable

from bysondb.base import BysonDBBase, is_bson_valid


class BysonDocumentDB(BysonDBBase):
    """
    A document-based database, which stores data in an object based format,
    which is similar to JSON.

    Example
    -----------
    ```
    my_db = BysonDocumentDB("my_db.bson")

    my_db.insert_one({"name": "John", "age": 42})

    for document in my_db.find({}):
        print(f"My name is {my_db['first_name']}, and I am {my_db['age']} years old")
    ```

    Parameters
    -----------
    file: str
        The name or path to the file where the database will store it's data.
        The file will be created if it does not exist, or existing data
        will be loaded.
    """

    def __init__(self, file: str) -> None:
        super().__init__(file, {"documents": []})

    def _get_documents(self) -> Iterable[dict]:
        """
        Fetch documents from memory.
        """

        return self._db["documents"]

    def _store_document(self, document: dict) -> None:
        """
        Stores documents into memory.
        """

        for item in document.items():
            if not is_bson_valid(item):
                raise InvalidTypeException(item)

        self._db["documents"].append(document)

    def insert_one(self, document: dict) -> None:
        """
        Insert a single document into the database.

        Parameters
        -----------
        document: dict
            The document to insert.
        """
        if isinstance(document, dict):
            self._store_document(document)
        else:
            raise TypeError("The document must be a dictionary.")
        self._dump()

    def insert_many(self, documents: Iterable[dict]) -> None:
        """
        Insert multiple documents, contained in an iterable.

        Parameters
        -----------
        documents: Iterable[dict]
            An iterable containing the documents to insert.
        """
        for i, document in enumerate(documents):
            if isinstance(document, dict):
                self._store_document(document)
            else:
                raise TypeError(
                    f"The document at index {i} was not a dictionary. All documents must be dictionaries."
                )
        self._dump()

    def _match(self, document: dict, query: dict) -> bool:
        """
        Checks to see if a document matches the query.
        """

        matches = [
            self._match(document.get(key), value)
            if isinstance(value, dict) and isinstance(document.get(key), dict)
            else document.get(key) == value
            for key, value in query.items()
        ]
        return all(matches)

    def find(
        self, query: dict, limit: Optional[int] = 0
    ) -> Union[Iterable[dict], dict]:
        """
        Find a document in the database based on a search query.

        Parameters
        -----------
        query: dict
            The search query.
        limit: Optional[int]
            A limit to the number of results to return. 0 means no limit.
            default: 0
        """

        self._load()

        matches = [
            document
            for document in self._get_documents()
            if self._match(document, query)
        ]

        if limit <= 0:
            limit = len(matches)

        return matches[: limit]

    def remove(self, query: dict, limit: Optional[int] = 0) -> None:
        """
        Remove documents from the database based on a search query.

        Parameters
        -----------
        query: dict
            The search query.
        limit: Optional[int]
            A limit to the number of results to return. 0 means no limit.
            default: 0
        """

        matches = self.find(query, limit)
        for match in matches:
            self._db["documents"].remove(match)

        self._dump()
