import inspect
import os
from typing import TYPE_CHECKING, Any

from openpyxl.styles import Font

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet
    from structlog._config import BoundLoggerLazyProxy

import click

from bam_data_store.utils import import_module


def entities_to_excel(
    worksheet: 'Worksheet',
    module_path: str,
    definitions_module: Any,
    logger: 'BoundLoggerLazyProxy',
) -> None:
    """
    Export entities to JSON files. The Python modules are imported using the function `import_module`,
    and their contents are inspected (using `inspect`) to find the classes in the datamodel containing
    `defs` and with a `to_json` method defined.

    Args:
        module_path (str): Path to the Python module file.
        export_dir (str): Path to the directory where the JSON files will be saved.
        logger (BoundLoggerLazyProxy): The logger to log messages.
    """
    def_members = inspect.getmembers(definitions_module, inspect.isclass)
    module = import_module(module_path=module_path)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure the class has the `to_json` method
        if not hasattr(obj, 'defs') or not callable(getattr(obj, 'to_json')):
            continue

        obj_instance = obj()

        # Entity title
        obj_definitions = obj_instance.defs
        worksheet.append([obj_definitions.excel_name])

        # Entity header definitions and values
        for def_name, def_cls in def_members:
            if def_name == obj_definitions.name:
                break
        worksheet.append(obj_definitions.excel_headers)
        header_values = [
            getattr(obj_definitions, f_set) for f_set in def_cls.model_fields.keys()
        ]
        worksheet.append(header_values)

        # Properties assignment for ObjectType
        if obj_instance.entity_type == 'ObjectType':
            if not obj_instance.properties:
                continue
            worksheet.append(obj_instance.properties[0].excel_headers)
            for prop in obj_instance.properties:
                worksheet.append(
                    getattr(prop, f_set) for f_set in prop.model_fields.keys()
                )
        # Terms assignment for VocabularyType
        elif obj_instance.entity_type == 'VocabularyType':
            if not obj_instance.terms:
                continue
            worksheet.append(obj_instance.terms[0].excel_headers)
            for term in obj_instance.terms:
                worksheet.append(
                    getattr(term, f_set) for f_set in term.model_fields.keys()
                )

        worksheet.append([''])  # empty row after entity definitions
