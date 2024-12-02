from typing import Any

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
)


class Model(BaseModel):
    a: str = Field(description='')

    @field_validator('a')
    @classmethod
    def ensure_foobar(cls, v: Any):
        if 'foobar' not in v:
            raise ValueError('"foobar" not found in a')
        return v


class ObjectType(BaseModel):
    # mandatory
    code: str = Field(
        description="""
        Code string identifying the object type with an openBIS inventory definition. Must be
        uppercase and separated by underscores.
        """,
    )

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: Any) -> Any:
        if not v:
            raise ValueError('Code must be uppercase and separated by underscore')
        return v


# model = Model(a='fuck')
object = ObjectType()
