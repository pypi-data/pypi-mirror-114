class InvalidTypeException(Exception):
    def __init__(self, value):
        self.type = type(value)

        super().__init__(
            self,
            f"Value of type {self.type} is not able to be serialized to BSON. Try using a different type or value.",
        )
