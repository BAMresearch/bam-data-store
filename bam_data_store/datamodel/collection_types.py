from bam_data_store.metadata.definitions import (
    CollectionTypeDef,
    PropertyTypeAssignment,
)
from bam_data_store.metadata.entities import CollectionType


class DefaultExperiment(CollectionType):
    defs = CollectionTypeDef(
        version=1,
        code='DEFAULT_EXPERIMENT',
        description="""
        Default Experiment//Standard-Experiment
        """,
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

    grant = PropertyTypeAssignment(
        version=1,
        code='DEFAULT_EXPERIMENT.GRANT',
        data_type='VARCHAR',
        property_label='Grant',
        description="""
        Grant
        """,
        mandatory=False,
        show_in_edit_views=True,
        section='General information',
    )

    experimental_goals = PropertyTypeAssignment(
        version=1,
        code='DEFAULT_EXPERIMENT.EXPERIMENTAL_GOALS',
        data_type='MULTILINE_VARCHAR',
        property_label='Goals',
        description="""
        Goals of the experiment
        """,
        mandatory=False,
        show_in_edit_views=True,
        section='Experimental details',
    )
