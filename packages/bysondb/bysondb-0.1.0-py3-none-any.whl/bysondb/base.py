from pathlib import Path
from typing import Optional, Union

import bson
from bson.codec import UnknownSerializerError


class BysonDBBase:
    """
    A base class, that contains the methods needed for both `BysonDB` and
    `BysonDocumentDB`, mostly for reading a writing to the database file.
    """

    def __init__(self, file: str, _db_default: Union[dict, list]):

        self.file = file
        self.path = Path(file).with_suffix(".bson")

        self._db = _db_default

        self._load_if_exists()

    def __str__(self) -> str:
        return f"<BysonDB file={self.path.resolve()} data={self._db}>"

    def _load_if_exists(self) -> None:
        """
        Loads the database file if it exists. If it does not exist, a new one
        is created.
        """
        try:
            self._db = self._load()
        except FileNotFoundError:
            self._dump()

    def _load(self) -> Optional[dict]:
        """
        Open the database file, and load the data stored in it.
        """

        byte_data = self.path.read_bytes()
        data = bson.loads(byte_data)

        return data

    def _dump(self) -> None:
        """
        Open the database file, and dump the current data to it. If the file
        does not exist, a new one is created.
        """

        if not self.path.exists():
            self.path.resolve().parent.mkdir(parents=True, exist_ok=True)

        data = bson.dumps(self._db)
        self.path.write_bytes(data)


def is_bson_valid(value) -> bool:
    """
    Checks if a value is able to be serialized into BSON.
    """

    try:
        bson.dumps({"value": value})
    except UnknownSerializerError:
        return False
    else:
        return True
