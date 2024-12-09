from bam_data_store.metadata.definitions import ObjectTypeDef, PropertyTypeAssignment
from bam_data_store.metadata.entities import ObjectType


class Instrument(ObjectType):
    defs = ObjectTypeDef(
        version=1,
        code='INSTRUMENT',
        description="""
        Measuring Instrument//Messger\u00e4t
        """,
        generated_code_prefix='INS',
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
        property_label='Alternative name',
        description="""
        e.g. abbreviation or nickname//z.B. Abkürzung oder Spitzname//z.B. Abkürzung oder Spitzname
        """,
        mandatory=False,
        show_in_edit_views=True,
        section='General information',
    )

    # ... other property types here...


class WeldingEquipment(Instrument):
    defs = ObjectTypeDef(
        version=1,
        code='INSTRUMENT.WELDING_EQUIPMENT',
        description="""
        Generic Welding Equipment//Unspezifisches Schweiß-Equipment
        """,
        generated_code_prefix='INS.WLD_EQP',
    )


class GMAWTorch(WeldingEquipment):
    defs = ObjectTypeDef(
        version=1,
        code='INSTRUMENT.WELDING_EQUIPMENT.GMAW_TORCH',
        description="""
        Arc welding torch for gas metal arc welding (GMAW) applications//Schweißbrenner für Metall-Schutzgas-Schweißen (MSG-Schweißen)
        """,
        generated_code_prefix='INS.WLD_EQP.GMAW_TRCH',
    )

    torch_type = PropertyTypeAssignment(
        version=1,
        code='WELDING.TORCH_TYPE',
        data_type='CONTROLLEDVOCABULARY',
        vocabulary_code='WELDING.GMAW_TORCH_TYPE',  # ? use only the class name?
        property_label='Type',
        description="""
        type of welding torch//Art des Schweißbrenners
        """,
        mandatory=True,
        show_in_edit_views=True,
        section='General information',
    )
