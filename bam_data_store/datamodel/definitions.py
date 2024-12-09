import re
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

# TODO check the other data types
DATA_TYPE_MAPPING: dict[str, type] = {
    'BOOLEAN': bool,
    # 'CONTROLLEDVOCABULARY': ,
    # 'DATE': ,
    'HYPERLINK': str,
    'INTEGER': int,
    # 'MATERIAL': ,
    'MULTILINE_VARCHAR': str,
    # 'OBJECT': ,
    'REAL': float,
    # 'TIMESTAMP': ,
    'VARCHAR': str,
    # 'XML': ,
}


class DataType(str, Enum):
    BOOLEAN = 'BOOLEAN'
    CONTROLLEDVOCABULARY = 'CONTROLLEDVOCABULARY'
    DATE = 'DATE'
    HYPERLINK = 'HYPERLINK'
    INTEGER = 'INTEGER'
    MATERIAL = 'MATERIAL'
    MULTILINE_VARCHAR = 'MULTILINE_VARCHAR'
    OBJECT = 'OBJECT'
    REAL = 'REAL'
    TIMESTAMP = 'TIMESTAMP'
    VARCHAR = 'VARCHAR'
    XML = 'XML'


class EntityDef(BaseModel):
    """
    Abstract base class for all masterdata entity definitions. The entity definitions are immutable properties.
    This class provides a common interface (with common attributes like `version`, `code` and
    `description`.) for all entity definitions.
    """

    version: int = Field(
        ...,
        description="""
        Version of the entity definition. This is an integer that is incremented each time the
        definition is changed.
        """,
    )  # ? is this useful?

    code: str = Field(
        ...,
        description="""
        Code string identifying the entity with an openBIS inventory definition. Must be
        uppercase and separated by underscores, e.g. `'EXPERIMENTAL_STEP'`.
        """,
    )

    description: str = Field(
        ...,
        description="""
        Description of the entity. This is the human-readable text for the object and must be
        as complete and concise as possible. The German description can be added after the English
        description separated by a double slash (//), e.g. `'Chemical Substance//Chemische Substanz'`.
        """,
    )

    # TODO check ontology_id, ontology_version, ontology_annotation_id, internal (found in the openBIS docu)

    @field_validator('code')
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value or not re.match(r'^[A-Z_\$\.]+$', value):
            raise ValueError('`code` must be uppercase and separated by underscores')
        return value


class BaseObjectTypeDef(EntityDef):
    """
    Definition class used for the common fields for `CollectionTypeDef`, `ObjectTypeDef`, and `DataSetType`.
    It adds the fields of `validation_script`.
    """

    validation_script: Optional[str] = Field(
        default=None,
        description="""
        Script written in Jython used to validate the object type.
        """,
    )  # ? is this truly used?


class CollectionTypeDef(BaseObjectTypeDef):
    """
    Definition class for a collection type. E.g.:

    ```python
    class DefaultExperiment(BaseModel):
        defs = CollectionTypeDef(
            version=1,
            code='DEFAULT_EXPERIMENT',
            description='',
            validation_script='DEFAULT_EXPERIMENT.date_range_validation',
        )
    ```
    """

    pass


class DataSetTypeDef(BaseObjectTypeDef):
    """
    Definition class for a data set type. E.g.:

    ```python
    class RawData(BaseModel):
        defs = DataSetTypeDef(
            version=1,
            code='RAW_DATA',
            description='',
        )
    """

    # TODO check descriptions

    main_dataset_pattern: Optional[str] = Field(
        default=None,
        description="""""",
    )

    main_dataset_path: Optional[str] = Field(
        default=None,
        description="""""",
    )


class ObjectTypeDef(BaseObjectTypeDef):
    """
    Definition class for an object type. It adds the fields of `generated_code_prefix`, `auto_generated_codes`,
    and `validation_script` to the common attributes of an entity definition. E.g.:

    ```python
    class Instrument(BaseModel):
        defs = ObjectTypeDef(
            version=1,
            code='INSTRUMENT',
            description='
            Measuring Instrument//Messger\u00e4t
            ',
            generated_code_prefix='INS',
        )
    ```
    """

    generated_code_prefix: Optional[str] = Field(
        default=None,
        description="""
        A short prefix for the defined object type, e.g. 'CHEM'. If not specified, it is defined
        using the first 3 characters of `code`.
        """,
    )

    auto_generated_codes: bool = Field(
        True,
        description="""
        Boolean used to generate codes using `generated_code_prefix` and a unique number. Set to
        True by default.
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
        if not data.generated_code_prefix:
            data.generated_code_prefix = data.code[:3]
        return data


class PropertyTypeDef(EntityDef):
    """
    Definition class for a property type. It adds the fields of `property_label`, `data_type`,
    `vocabulary_code`, `metadata`, `dynamic_script`, and `multivalued` to the common attributes of
    an entity definition. E.g.:

    ```python
    class Alias(PropertyTypeDef):
        defs = PropertyTypeDef(
            version=1,
            code='ALIAS',
            description='
            e.g. abbreviation or nickname//z.B. Abkürzung oder Spitzname//z.B. Abkürzung oder Spitzname
            ',
            data_type='VARCHAR',
            property_label='Alternative name',
        )
    ```
    """

    property_label: str = Field(
        ...,
        description="""
        Label that appears in the inventory view. This is the human-readable text for the property
        type definition, and it typically coincides with the `code`, e.g., `'Monitoring date'` for the
        `MONITORING_DATE` property type.
        """,
    )

    data_type: DataType = Field(
        ...,
        description="""
        The data type of the property, i.e., if it is an integer, float, string, etc. The allowed
        data types in openBIS are:
            - `BOOLEAN`
            - `CONTROLLEDVOCABULARY`
            - `DATE`
            - `HYPERLINK`
            - `INTEGER`
            - `MATERIAL`
            - `MULTILINE_VARCHAR`
            - `OBJECT`
            - `REAL`
            - `TIMESTAMP`
            - `VARCHAR`
            - `XML`

        These are defined as an enumeration in the `DataType` class.

        Read more in https://openbis.readthedocs.io/en/latest/uncategorized/register-master-data-via-the-admin-interface.html#data-types-available-in-openbis.
        """,
    )

    vocabulary_code: Optional[str] = Field(
        default=None,
        description="""
        String identifying the controlled vocabulary used for the data type of the property. This is
        thus only relevant if `data_type == 'CONTROLLEDVOCABULARY'`.
        """,
    )

    metadata: Optional[dict] = Field(
        default=None,
        description="""""",
    )

    dynamic_script: Optional[str] = Field(
        default=None,
        description="""""",
    )

    multivalued: Optional[str] = Field(
        default=None,
        description="""""",
    )


class PropertyTypeAssignment(PropertyTypeDef):
    """
    aaa
    """

    mandatory: bool = Field(
        ...,
        description="""
        If `True`, the property is mandatory and has to be set during instantiation of the object type.
        If `False`, the property is optional.
        """,
    )

    show_in_edit_views: bool = Field(
        ...,
        description="""
        If `True`, the property is shown in the edit views of the ELN in the object type instantiation.
        If `False`, the property is hidden.
        """,
    )

    section: str = Field(
        ...,
        description="""
        Section to which the property type belongs to. E.g., `'General Information'`.
        """,
    )

    unique: Optional[str] = Field(
        default=None,
        description="""""",
    )

    internal_assignment: Optional[str] = Field(
        default=None,
        description="""""",
    )


class VocabularyTypeDef(EntityDef):
    """
    Definition class for a vocabulary type. E.g.:
    """

    url_template: Optional[str] = Field(
        default=None,
        description="""""",
    )


class VocabularyTerm(VocabularyTypeDef):
    """
    aaa
    """

    label: str = Field(
        ...,
        description="""""",
    )

    official: bool = Field(
        True,
        description="""""",
    )
