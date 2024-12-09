from typing import Optional

import pytest

from bam_data_store.metadata.definitions import (
    BaseObjectTypeDef,
    CollectionTypeDef,
    DataSetTypeDef,
    DataType,
    EntityDef,
    ObjectTypeDef,
    PropertyTypeAssignment,
    PropertyTypeDef,
    VocabularyTerm,
    VocabularyTypeDef,
)


class TestDataType:
    @pytest.mark.parametrize(
        'data_type, result',
        [
            (DataType.BOOLEAN, bool),
            (
                DataType.CONTROLLEDVOCABULARY,
                None,
            ),  # Update this once the mapping is implemented
            (DataType.DATE, None),  # Update this once the mapping is implemented
            (DataType.HYPERLINK, str),
            (DataType.INTEGER, int),
            (DataType.MATERIAL, None),  # Update this once the mapping is implemented
            (DataType.MULTILINE_VARCHAR, str),
            (DataType.OBJECT, None),  # Update this once the mapping is implemented
            (DataType.REAL, float),
            (DataType.TIMESTAMP, None),  # Update this once the mapping is implemented
            (DataType.VARCHAR, str),
            (DataType.XML, None),  # Update this once the mapping is implemented
        ],
    )
    def test_pytype(self, data_type: DataType, result: type):
        """Test the `pytype` property of `DataType`."""
        assert data_type.pytype == result


class TestEntityDef:
    def test_fields(self):
        """Test the existing defined fields of the `EntityDef` class."""
        names = list(EntityDef.model_fields.keys())
        field_types = [val.annotation for val in list(EntityDef.model_fields.values())]
        assert names == ['version', 'code', 'description']
        assert field_types == [int, str, str]

    @pytest.mark.parametrize(
        'version, code, description, is_valid',
        [
            # `code` in capital and separated by underscores
            (1, 'EXPERIMENTAL_STEP', 'Valid description', True),
            # `code` starting with $ symbol
            (1, '$NAME', 'Valid description', True),
            # `code` separating inheritance with points
            (1, 'WELDING_EQUIPMENT.INSTRUMENT', 'Valid description', True),
            # Invalid `code`
            (1, 'INVALID CODE', 'Valid description', False),
            # `description` is not a string
            (1, 'EXPERIMENTAL_STEP', 2, False),
            # Empty `code`
            (1, '', 'Valid description', False),
            # Missing `version`
            (None, 'EXPERIMENTAL_STEP', 'Valid description', False),
        ],
    )
    def test_entity_def(
        self, version: int, code: str, description: str, is_valid: bool
    ):
        """Test creation of `EntityDef` and field validation."""
        if is_valid:
            entity = EntityDef(version=version, code=code, description=description)
            assert entity.version == version
            assert entity.code == code
            assert entity.description == description
        else:
            with pytest.raises(ValueError):
                EntityDef(version=version, code=code, description=description)

    @pytest.mark.parametrize(
        'code, is_valid',
        [
            # `code` in capital and separated by underscores
            ('EXPERIMENTAL_STEP', True),
            # `code` starting with $ symbol
            ('$NAME', True),
            # `code` separating inheritance with points
            ('WELDING_EQUIPMENT.INSTRUMENT', True),
            # Invalid `code`
            ('INVALID CODE', False),
            # Empty code
            ('', False),
        ],
    )
    def test_validate_code(self, code: str, is_valid: bool):
        """Test the code validator."""
        if is_valid:
            entity = EntityDef(version=1, code=code, description='Valid description')
            assert entity.code == code
        else:
            with pytest.raises(ValueError):
                EntityDef(version=1, code=code, description='Valid description')

    def test_strip_description(self):
        """Test the `strip_description` method."""
        entity = EntityDef(
            version=1, code='EXPERIMENTAL_STEP', description='  Valid description  '
        )
        assert entity.description == 'Valid description'


class TestBaseObjectTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `BaseObjectTypeDef` class."""
        names = list(BaseObjectTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(BaseObjectTypeDef.model_fields.values())
        ]
        assert names == ['version', 'code', 'description', 'validation_script']
        assert field_types == [int, str, str, Optional[str]]


class TestCollectionTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `CollectionTypeDef` class."""
        names = list(CollectionTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(CollectionTypeDef.model_fields.values())
        ]
        assert names == ['version', 'code', 'description', 'validation_script']
        assert field_types == [int, str, str, Optional[str]]


class TestDataSetTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `DataSetTypeDef` class."""
        names = list(DataSetTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(DataSetTypeDef.model_fields.values())
        ]
        assert names == [
            'version',
            'code',
            'description',
            'validation_script',
            'main_dataset_pattern',
            'main_dataset_path',
        ]
        assert field_types == [
            int,
            str,
            str,
            Optional[str],
            Optional[str],
            Optional[str],
        ]


class TestObjectTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `ObjectTypeDef` class."""
        names = list(ObjectTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(ObjectTypeDef.model_fields.values())
        ]
        assert names == [
            'version',
            'code',
            'description',
            'validation_script',
            'generated_code_prefix',
            'auto_generated_codes',
        ]
        assert field_types == [int, str, str, Optional[str], Optional[str], bool]

    @pytest.mark.parametrize(
        'code, generated_code_prefix, result',
        [
            # No `generated_code_prefix`
            ('INSTRUMENT', None, 'INS'),
            ('INSTRUMENT', '', 'INS'),
            # `generated_code_prefix` is already set
            ('INSTRUMENT', 'INSTRU', 'INSTRU'),
        ],
    )
    def test_model_validator_after_init(
        self, code: str, generated_code_prefix: Optional[str], result: str
    ):
        """Test the after-init model validator for `ObjectTypeDef`."""
        entity = ObjectTypeDef(
            version=1,
            code=code,
            description='Valid description',
            generated_code_prefix=generated_code_prefix,
        )
        assert entity.generated_code_prefix == result


class TestPropertyTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `PropertyTypeDef` class."""
        names = list(PropertyTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(PropertyTypeDef.model_fields.values())
        ]
        assert names == [
            'version',
            'code',
            'description',
            'property_label',
            'data_type',
            'vocabulary_code',
            'metadata',
            'dynamic_script',
            'multivalued',
        ]
        assert field_types == [
            int,
            str,
            str,
            str,
            DataType,
            Optional[str],
            Optional[dict],
            Optional[str],
            Optional[str],
        ]


class TestPropertyTypeAssignment:
    def test_fields(self):
        """Test the existing defined fields of the `PropertyTypeAssignment` class."""
        names = list(PropertyTypeAssignment.model_fields.keys())
        field_types = [
            val.annotation for val in list(PropertyTypeAssignment.model_fields.values())
        ]
        assert names == [
            'version',
            'code',
            'description',
            'property_label',
            'data_type',
            'vocabulary_code',
            'metadata',
            'dynamic_script',
            'multivalued',
            'mandatory',
            'show_in_edit_views',
            'section',
            'unique',
            'internal_assignment',
        ]
        assert field_types == [
            int,
            str,
            str,
            str,
            DataType,
            Optional[str],
            Optional[dict],
            Optional[str],
            Optional[str],
            bool,
            bool,
            str,
            Optional[str],
            Optional[str],
        ]


class TestVocabularyTypeDef:
    def test_fields(self):
        """Test the existing defined fields of the `VocabularyTypeDef` class."""
        names = list(VocabularyTypeDef.model_fields.keys())
        field_types = [
            val.annotation for val in list(VocabularyTypeDef.model_fields.values())
        ]
        assert names == ['version', 'code', 'description', 'url_template']
        assert field_types == [int, str, str, Optional[str]]


class TestVocabularyTerm:
    def test_fields(self):
        """Test the existing defined fields of the `VocabularyTerm` class."""
        names = list(VocabularyTerm.model_fields.keys())
        field_types = [
            val.annotation for val in list(VocabularyTerm.model_fields.values())
        ]
        assert names == [
            'version',
            'code',
            'description',
            'url_template',
            'label',
            'official',
        ]
        assert field_types == [int, str, str, Optional[str], str, bool]
