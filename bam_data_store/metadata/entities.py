import json
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bam_data_store.metadata.definitions import (
    ObjectTypeDef,
    PropertyTypeAssignment,
    VocabularyTerm,
    VocabularyTypeDef,
)


class BaseEntity(BaseModel):
    """
    Base class used to define `ObjectType` and `VocabularyType` classes. It extends the `BaseModel`
    adding new methods that are useful for interfacing with openBIS.
    """

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Returns the model as a string in JSON format storing the data `defs` and the property or
        vocabulary term assignments.

        Args:
            indent (Optional[int], optional): The indent to print in JSON. Defaults to None.

        Returns:
            str: The JSON representation of the model.
        """
        # * `model_dump_json()` from pydantic does not store the `defs` section of each entity.
        data = self.model_dump()

        attr_value = getattr(self, 'defs')
        if isinstance(attr_value, BaseModel):
            data['defs'] = attr_value.model_dump()
        else:
            data['defs'] = attr_value

        return json.dumps(data, indent=indent)

    def to_dict(self) -> dict:
        """
        Returns the model as a dictionary storing the data `defs` and the property or vocabulary term
        assignments.

        Returns:
            dict: The dictionary representation of the model.
        """
        dump_json = self.to_json()
        return json.loads(dump_json)


class ObjectType(BaseEntity):
    """
    Base class used to define object types. All object types must inherit from this class. The
    object types are defined in the module `bam_data_store/object_types.py`.

    The `ObjectType` class contains a list of all `properties` defined for a `ObjectType`, for
    internally represent the model in other formats (e.g., JSON or Excel).
    """

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


class VocabularyType(BaseEntity):
    """
    Base class used to define vocabulary types. All vocabulary types must inherit from this class. The
    vocabulary types are defined in the module `bam_data_store/vocabulary_types.py`.

    The `VocabularyType` class contains a list of all `terms` defined for a `VocabularyType`, for
    internally represent the model in other formats (e.g., JSON or Excel).
    """

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


class PropertyType(BaseEntity):
    pass


class CollectionType(BaseEntity):
    pass
