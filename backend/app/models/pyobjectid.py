from typing import Any
from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value

        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)