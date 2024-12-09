from bam_data_store.metadata.definitions import (
    VocabularyTerm,
    VocabularyTypeDef,
)
from bam_data_store.metadata.entities import VocabularyType


class DocumentType(VocabularyType):
    defs = VocabularyTypeDef(
        version=1,
        code='DOCUMENT_TYPE',
        description='Document type//Dokumententypen',
    )

    acceptance_certificate = VocabularyTerm(
        version=1,
        code='ACCEPTANCE_CERTIFICATE',
        label='Acceptance Certificate',
        description='Acceptance Certificate//Abnahmezeugnis',
    )

    calibration_certificate = VocabularyTerm(
        version=1,
        code='CALIBRATION_CERTIFICATE',
        label='Calibration Certificate',
        description='Calibration Certificate//Kalibrierschein',
    )

    catalog = VocabularyTerm(
        version=1,
        code='CATALOG',
        label='Catalog',
        description='Document type//Dokumententypen',
    )

    datasheet = VocabularyTerm(
        version=1,
        code='DATASHEET',
        label='Datasheet',
        description='Datasheet//Datenblatt',
    )

    datasheet_msds = VocabularyTerm(
        version=1,
        code='DATASHEET_MSDS',
        label='Material Safety Datasheet',
        description='Material Safety Datasheet (MSDS)//Sicherheitsdatenblatt',
    )

    datasheet_technical = VocabularyTerm(
        version=1,
        code='DATASHEET_TECHNICAL',
        label='Technical Datasheet',
        description='Technical Datasheet//Technisches Datenblatt',
    )

    delivery_note = VocabularyTerm(
        version=1,
        code='DELIVERY_NOTE',
        label='Delivery Note',
        description='Delivery Note//Lieferschein',
    )

    diagram = VocabularyTerm(
        version=1,
        code='DIAGRAM',
        label='Diagram',
        description='Diagram//Diagramm',
    )

    fabrication_order = VocabularyTerm(
        version=1,
        code='FABRICATION_ORDER',
        label='Fabrication Order',
        description='Fabrication Order//Fertigungsauftrag',
    )

    inspection_certificate = VocabularyTerm(
        version=1,
        code='INSPECTION_CERTIFICATE',
        label='Inspection Certificate',
        description='Inspection Certificate//Inspektionszeugnis',
    )
