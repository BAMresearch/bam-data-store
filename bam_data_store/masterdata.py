from typing import ClassVar

from pydantic import BaseModel, Field

from bam_data_store.definitions import (
    MasterdataDefinitions,
    ObjectTypeDefinitions,
)


class Masterdata(BaseModel):
    """
    aa
    """

    # definitions: ClassVar[MasterdataDefinitions] = MasterdataDefinitions(
    #     code='MASTERDATA',
    #     description="""
    #     Mockup description for the abstract `Masterdata` class. This needs to be overwritten when inheriting
    #     in the definitions.
    #     """,
    # )

    pass


class ObjectType(Masterdata):
    """
    object type class
    """

    definitions: ClassVar[ObjectTypeDefinitions] = ObjectTypeDefinitions(
        code='OBJECT_TYPE',
        description="""
        Mockup description for an `ObjectType` class. This needs to be overwritten when inheriting
        in the definitions.
        """,
        generated_code_prefix='OBJT',
    )


class Chemical(ObjectType):
    """ """

    definitions = ObjectTypeDefinitions(
        code='CHEMICAL',
        description="""
        Chemical Substance//Chemische Substanz
        """,
        generated_code_prefix='CHEM',
        auto_generated_codes=False,
    )


class Instrument(ObjectType):
    sensor_name: str = Field(..., description="""...""")

    prop2: str = Field('default', description="""...""")

    prop3: str = Field(description="""...""")

    chemical: list[Chemical] = Field(description="""...""")


class Camera(Instrument):
    pass


chemical = Chemical()
print('hey')


# class PropertyType(Masterdata):
#     code: str = Field(description='')
#     mandatory: bool = Field(description='')
#     show_in_edit_views: bool = Field(description='')
#     section: str = Field(description='')
#     property_label: str = Field(description='')
#     data_type: str = Field(description='')
