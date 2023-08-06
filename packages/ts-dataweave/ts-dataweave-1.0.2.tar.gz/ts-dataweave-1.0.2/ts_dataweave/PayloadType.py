from enum import Enum, unique

@unique
class PayloadType(str, Enum):
    """DataWeave payload type
    """

    JSON = "json",
    CSV = "csv",
    XML = "xml"

    def __str__(self):
        return self.value
