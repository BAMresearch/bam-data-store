import re
from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class MasterdataDefinitions(BaseModel):
    """
    Base class for all masterdata definition attributes. There are some shared attributes (`code`, `description`, etc.)
    for the different entities, `ObjectType`, `PropertyType`, `VocabularyType`.

    This class is abstract and should not be instantiated directly. It provides a common interface
    for all masterdata definitions.
    """

    code: str = Field(
        ...,
        description="""
        Code string identifying the masterdata entity with an openBIS inventory definition. Must be
        uppercase and separated by underscores, e.g.:

        ```python
        class ExperimentalStep(ObjectType):
            code: str = Field('EXPERIMENTAL_STEP')
        ```
        """,
    )

    description: str = Field(
        ...,
        description="""
        Description of the object type. This is the human-readable text for the object and must be
        as complete and concise as possible. The German description can be added after the English
        description separated by a double slash (//), e.g.:

        ```python
        class Chemical(ObjectType):
            description: str = Field('Chemical Substance//Chemische Substanz')
        ```
        """,
    )

    ontology_id: Optional[str] = Field(default=None, description='')

    ontology_version: Optional[str] = Field(default=None, description='')

    ontology_annotation_id: Optional[str] = Field(default=None, description='')

    internal: Optional[bool] = Field(default=None, description='')

    @field_validator('code')
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value or not re.match(r'^[A-Z_]+$', value):
            raise ValueError('`code` must be uppercase and separated by underscores')
        return value

    @abstractmethod
    def model_renormalize(self) -> None:
        pass


class ObjectTypeDefinitions(MasterdataDefinitions):
    """
    object type class
    """

    generated_code_prefix: str = Field(
        ...,
        description="""
        A short prefix for the defined object type, e.g.:

        ```python
        class Chemical(ObjectType):
            generated_code_prefix: str = Field('CHEM')
        ```
        """,
    )  # ! this is useless (`code` is itself already a good code identifier)

    auto_generated_codes: bool = Field(
        True,
        description="""
        Boolean to rewrite the `generated_code_prefix` using the first three letters of the `code`.
        """,
    )

    validation_script: str = Field('', description='')  # ? is this truly used?

    @model_validator(mode='after')
    @classmethod
    def model_validator_after_init(cls, data: Any) -> Any:
        if data.auto_generated_codes and data.code:
            data.generated_code_prefix = data.code[:4]
        return data

    def model_renormalize(self) -> None:
        pass
