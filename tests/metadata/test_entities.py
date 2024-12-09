from tests.conftest import (
    generate_base_entity,
    generate_object_type,
    generate_object_type_longer,
    generate_vocabulary_type,
)


class TestBaseEntity:
    def test_to_json(self):
        """Test the method `to_json` from the class `BaseEntity`."""
        entity = generate_base_entity()
        assert (
            entity.to_json()
            == '{"defs": {"version": 1, "code": "MOCKED_ENTITY", "description": "Mockup for an entity definition//Mockup f\\u00fcr eine Entit\\u00e4tsdefinition", "validation_script": null, "generated_code_prefix": "MOCKENT", "auto_generated_codes": true}}'
        )

    def test_to_dict(self):
        """Test the method `to_dict` from the class `BaseEntity`."""
        entity = generate_base_entity()
        assert entity.to_dict() == {
            'defs': {
                'version': 1,
                'code': 'MOCKED_ENTITY',
                'description': 'Mockup for an entity definition//Mockup für eine Entitätsdefinition',
                'validation_script': None,
                'generated_code_prefix': 'MOCKENT',
                'auto_generated_codes': True,
            }
        }


class TestObjectType:
    def test_model_validator_after_init(self):
        """Test the method `model_validator_after_init` from the class `ObjectType`."""
        # 2 properties in this `ObjectType`
        object_type = generate_object_type()
        assert len(object_type.properties) == 2
        prop_names = [prop.code for prop in object_type.properties]
        assert prop_names == ['ALIAS', '$NAME']

        # 3 properties in this `ObjectType`
        object_type = generate_object_type_longer()
        assert len(object_type.properties) == 3
        prop_names = [prop.code for prop in object_type.properties]
        assert prop_names == ['ALIAS', '$NAME', 'SETTINGS']


class TestVocabularyType:
    def test_model_validator_after_init(self):
        """Test the method `model_validator_after_init` from the class `VocabularyType`."""
        vocabulary_type = generate_vocabulary_type()
        assert len(vocabulary_type.terms) == 2
        term_names = [term.code for term in vocabulary_type.terms]
        assert term_names == ['OPTION_A', 'OPTION_B']
