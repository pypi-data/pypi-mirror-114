from __future__ import annotations

from secrets import token_bytes
import time

from pydantic.errors import PydanticTypeError
import cyksuid.ksuid


class KSUID(cyksuid.ksuid.KSUID):
    def __init__(self, *args, **kwargs):
        super(KSUID, self).__init__(*args, **kwargs)

    @staticmethod
    def new(time_func=time.time, rand_func=token_bytes) -> KSUID:
        return KSUID(cyksuid.ksuid.ksuid(time_func, rand_func).bytes)

    @staticmethod
    def from_timestamp(ts) -> KSUID:
        time_func = lambda: ts 
        return KSUID.new(time_func=time_func)

    @staticmethod
    def parse(data) -> KSUID:
        data = cyksuid.ksuid.parse(data)
        return KSUID(data.bytes)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string', format='ksuid')

    @classmethod
    def validate(cls, v):
        try:
            if isinstance(v, str):
                v = KSUID.parse(v)
            elif isinstance(v, (bytes, bytearray)):
                v = KSUID(v)
        except TypeError:
            raise KSUIDError

        if not isinstance(v, KSUID):
            raise KSUIDError

        return v

class KSUIDError(PydanticTypeError):
    msg_template = 'value is not a valid ksuid'
