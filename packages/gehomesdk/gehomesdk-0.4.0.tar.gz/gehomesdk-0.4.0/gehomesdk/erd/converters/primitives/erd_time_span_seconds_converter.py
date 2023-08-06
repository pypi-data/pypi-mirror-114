import logging

from datetime import timedelta
from typing import Optional

from ..abstract import ErdReadWriteConverter, ErdReadOnlyConverter
from gehomesdk.erd.erd_codes import ErdCodeType

_LOGGER = logging.getLogger(__name__)

def erd_decode_timespan_seconds(value: any) -> Optional[timedelta]:
    """ Decodes a raw integer (seconds) as a time span, 65535 is treated as None. """
    seconds = int(value, 16)
    if seconds == 65535:
        _LOGGER.debug('Got timespan value of 65535. Treating as None.')
        return None
    return timedelta(seconds=seconds)
def erd_encode_timespan_seconds(value: Optional[timedelta], length: int = 4) -> str:
    """ Encodes a time span as an erd integer (seconds) , None is encoded as 65535. """
    if value is None:
        seconds = 65535
    else:
        seconds = value.seconds
    return seconds.to_bytes(length, 'big').hex()    

class ErdTimeSpanSecondsConverter(ErdReadWriteConverter[Optional[timedelta]]):
    def __init__(self, erd_code: ErdCodeType = "Unknown", length: int = 4):
        super().__init__(erd_code)
        self.length = length        
    def erd_decode(self, value: str) -> Optional[timedelta]:
        """ Decodes a raw integer (seconds) as a time span, 65535 is treated as None. """
        return erd_decode_timespan_seconds(value)
    def erd_encode(self, value: Optional[timedelta]) -> str:
        """ Encodes a time span as an erd integer (seconds), None is encoded as 65535. """
        return erd_encode_timespan_seconds(value, self.length)

class ErdReadOnlyTimeSpanSecondsConverter(ErdReadOnlyConverter[Optional[timedelta]]):
    def erd_decode(self, value: str) -> Optional[timedelta]:
        """ Decodes a raw integer (seconds) as a time span, 65535 is treated as None. """
        return erd_decode_timespan_seconds(value)

