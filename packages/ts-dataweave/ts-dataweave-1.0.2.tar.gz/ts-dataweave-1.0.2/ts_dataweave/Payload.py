from io import BufferedIOBase
from typing import Union

from .PayloadType import PayloadType

class Payload:
    """DataWeave payload.
    """

    def __init__(self, payloadType: PayloadType, data: Union[dict, str, bytes, BufferedIOBase]):
        """Creates a new DataWeave payload instance.

        Args:
            payloadType (DataWeavePayloadType): payload content type
            data (Union[str, bytes, BufferedIOBase]): payload data as string, bytes, or file-like object
        """
        
        self.payloadType = payloadType
        self.data = data
