import os

import pytest
from pydantic import ConfigDict

from bam_data_store.logger import log_storage
from bam_data_store.metadata.definitions import (
    ObjectTypeDef,
    PropertyTypeAssignment,
    VocabularyTerm,
    VocabularyTypeDef,
)
from bam_data_store.metadata.entities import BaseEntity, ObjectType, VocabularyType

if os.getenv('_PYTEST_RAISE', '0') != '0':

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value


@pytest.fixture(autouse=True)
def cleared_log_storage():
    """Fixture to clear the log storage before each test."""
    log_storage.clear()
    yield log_storage


class MockedEntity(BaseEntity):
    model_config = ConfigDict(ignored_types=(ObjectTypeDef, PropertyTypeAssignment))
    defs = ObjectTypeDef(
        version=1,
        code='MOCKED_ENTITY',
        description="""
        Mockup for an entity definition//Mockup für eine Entitätsdefinition
        """,
        generated_code_prefix='MOCKENT',
    )

    name = PropertyTypeAssignment(
        version=1,
        code='$NAME',
        data_type='VARCHAR',
        property_label='Name',
        description="""
        Name
        """,
        mandatory=True,
        show_in_edit_views=True,
        section='General information',
    )


class MockedObjectType(ObjectType):
    defs = ObjectTypeDef(
        version=1,
        code='MOCKED_OBJECT_TYPE',
        description="""
        Mockup for an object type definition
        """,
        generated_code_prefix='MOCKOBJTYPE',
    )

    name = PropertyTypeAssignment(
        version=1,
        code='$NAME',
        data_type='VARCHAR',
        property_label='Name',
        description="""
        Name
        """,
        mandatory=True,
        show_in_edit_views=True,
        section='General information',
    )

    alias = PropertyTypeAssignment(
        version=1,
        code='ALIAS',
        data_type='VARCHAR',
        property_label='Alias',
        description="""
        Alias
        """,
        mandatory=False,
        show_in_edit_views=True,
        section='General information',
    )


class MockedObjectTypeLonger(MockedObjectType):
    defs = ObjectTypeDef(
        version=1,
        code='MOCKED_OBJECT_TYPE_LONGER',
        description="""
        Mockup for an object type definition with more property type assignments
        """,
        generated_code_prefix='MOCKOBJTYPELONG',
    )

    settings = PropertyTypeAssignment(
        version=1,
        code='SETTINGS',
        data_type='MULTILINE_VARCHAR',
        property_label='Settings',
        description="""
        Settings
        """,
        mandatory=False,
        show_in_edit_views=True,
        section='General information',
    )


class MockedVocabularyType(VocabularyType):
    defs = VocabularyTypeDef(
        version=1,
        code='MOCKED_VOCABULARY_TYPE',
        description="""
        Mockup for an vocabulary type definition
        """,
    )

    option_a = VocabularyTerm(
        version=1,
        code='OPTION_A',
        label='Option A',
        description='Option A from two possible options in the vocabulary',
    )

    option_b = VocabularyTerm(
        version=1,
        code='OPTION_B',
        label='Option B',
        description='Option B from two possible options in the vocabulary',
    )


def generate_base_entity():
    return MockedEntity()


def generate_object_type():
    return MockedObjectType()


def generate_object_type_longer():
    return MockedObjectTypeLonger()


def generate_vocabulary_type():
    return MockedVocabularyType()
