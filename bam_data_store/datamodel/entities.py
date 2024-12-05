import json
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bam_data_store.datamodel.definitions import (
    ObjectTypeDef,
    PropertyTypeAssignment,
    VocabularyTerm,
    VocabularyTypeDef,
)


class BaseEntity(BaseModel):
    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Returns the JSON representation of the model storing the data `defs` and the property or
        vocabulary term assignments.

        Args:
            indent (Optional[int], optional): The indent to print in JSON. Defaults to None.

        Returns:
            str: The JSON representation of the model.
        """
        data = self.model_dump()

        attr_value = getattr(self, 'defs')
        if isinstance(attr_value, BaseModel):
            data['defs'] = attr_value.model_dump()
        else:
            data['defs'] = attr_value

        return json.dumps(data, indent=indent)


class VocabularyType(BaseEntity):
    model_config = ConfigDict(ignored_types=(VocabularyTypeDef, VocabularyTerm))

    terms: list[VocabularyTerm] = Field(
        default=[],
        description="""
        List of vocabulary terms. This is useful for internal representation of the model.
        """,
    )

    @model_validator(mode='after')
    @classmethod
    def model_validator_after_init(cls, data: Any) -> Any:
        """
        Validate the model after instantiation of the class.

        Args:
            data (Any): The data containing the fields values to validate.

        Returns:
            Any: The data with the validated fields.
        """
        # Add all the vocabulary terms defined in the vocabulary type to the `terms` list.
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, VocabularyTerm):
                data.terms.append(attr)
        return data


class ObjectType(BaseModel):
    model_config = ConfigDict(ignored_types=(ObjectTypeDef, PropertyTypeAssignment))

    properties: list[PropertyTypeAssignment] = Field(
        default=[],
        description="""
        List of properties assigned to an object type. This is useful for internal representation of the model.
        """,
    )

    @model_validator(mode='after')
    @classmethod
    def model_validator_after_init(cls, data: Any) -> Any:
        """
        Validate the model after instantiation of the class.

        Args:
            data (Any): The data containing the fields values to validate.

        Returns:
            Any: The data with the validated fields.
        """
        # Add all the properties assigned to the object type to the `properties` list.
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, PropertyTypeAssignment):
                data.properties.append(attr)
        return data
