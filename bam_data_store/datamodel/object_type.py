from bam_data_store.datamodel.definitions import ObjectTypeDef, PropertyTypeAssignment
from bam_data_store.datamodel.entities import ObjectType


class Instrument(ObjectType):
    defs = ObjectTypeDef(
        version=1,
        code='INSTRUMENT',
        description="""
        Measuring Instrument//Messger\u00e4t
        """,
        generated_code_prefix='INS',
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
        section='General',
    )
